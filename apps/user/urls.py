from django.urls import re_path
from user.views import VxTest

urlpatterns = [
    re_path('vx_test/', VxTest.as_view()),
]