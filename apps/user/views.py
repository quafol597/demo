from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView


class VxTest(APIView):
    def get(self, request):
        query_params = request.query_params
        data = request.data
        print(query_params)
        print(data)
        return JsonResponse({'code': 0, 'errmsg': 'ok'})
