from django.urls import re_path
from .views import BookView

urlpatterns = [
    re_path(r'enterprise/$', BookView.as_view()),
]