import binascii
import json

from rest_framework.response import Response
from rest_framework.views import APIView

from enterprise.models import TbOfEnt
from myrsa2.apiutils import APIUtils


class BookView(APIView):

    def get(self, request):
        key_obj = TbOfEnt.objects.get(pk=1)

        apiutils = APIUtils(appid=key_obj.appid,
                            oppsite_pub_key_string=key_obj.oppsite_pub_key,  # 对方的公钥 --> 验签
                            my_pri_key_string=key_obj.app_priv_key,  # 自己的私钥 --> 签名
                            sign_type='RSA2')

        content = apiutils.api_apiutils_books(subject='得到所有图书')

        result = content['result']
        signature = content['signature']

        if apiutils.verify(result, signature):
            return Response({'result': result})

        return Response({'msg': '验签失败'})


