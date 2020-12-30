import json
import rsa
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from myrsa2.apiutils import APIUtils
from myrsa2.models import App
from myrsa2.serializers import KeymanagerSerializer


class KeymanagertViewSet(RetrieveModelMixin,
                         UpdateModelMixin,
                         GenericViewSet): # ViewSetMixin GenericAPIView APIView
    queryset = App.objects.all()
    serializer_class = KeymanagerSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if not instance.oppsite_pub_key and not instance.plat_pri_key:
            # 如果app对象plat_pub_key和plat_pri_key属性为空: 则生成公私钥写入数据库.
            pub_key, priv_key = self.gen_rsa_keys()
            instance.oppsite_pub_key = pub_key
            instance.plat_pri_key = priv_key
            instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @staticmethod
    def gen_rsa_keys() -> (str, str):
        """生成公私钥字符串"""
        (pub_obj, priv_obj) = rsa.newkeys(2048)
        pub_key = pub_obj.save_pkcs1().decode()
        priv_key = priv_obj.save_pkcs1().decode()

        return pub_key, priv_key


class GateWayView(APIView):

    def post(self, request):

        # <1> 验签
        body_str = request.data.get('body')
        signature = request.data.get('signature')
        body = json.loads(body_str)

        app_id = body.get('app_id')
        try:
            app = App.objects.get(app_id=app_id)  # 此时尚未验签, app_id可能被篡改
        except App.DoesNotExist:
            return Response({'msg': '信息有误, 请重新发送.'})

        apiutils = APIUtils(appid=app_id,
                            oppsite_pub_key_string=app.ent_pub_key,
                            my_pri_key_string=app.plat_pri_key,
                            sign_type='RSA2')

        if not apiutils.verify(body, signature):
            return Response({'msg': '验签失败'})

        # <2> 构造响应 -> {'body': body, 'signature': 'alsdkfjlaskjdf'}
        # body = {'app_id': '202010140123456',
        #         'charset': 'utf-8',
        #         'sign_type': 'RSA2',
        #         'timestamp': '2020-10-15 14:43:38',
        #         'version': '1.0',
        #         'biz_content': '{"subject":"得到所有图书"}',
        #         'method': 'api_apiutils_books'}

        # 通过method确定用户需要访问的接口
        method = body.get('method')
        if method == 'api_apiutils_books':
            result, signature = self.api_apiutils_books(apiutils)
            return Response({'result': result, 'signature': signature})

    def api_apiutils_books(self, apiutils):
        from book_hero.models import BookInfo
        from book_hero.serializers import BookSerializer

        querydict = BookInfo.objects.all()
        serializer = BookSerializer(querydict, many=True)
        content = [dict(item) for item in serializer.data]
        result = apiutils.build_body(content)
        signature = apiutils.sign_data(result)
        return result, signature
