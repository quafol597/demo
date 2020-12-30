from django.urls import re_path
from .views import KeymanagertViewSet, GateWayView

urlpatterns = [
    re_path(r'keymanager/(?P<pk>\d+)/$', KeymanagertViewSet.as_view({'get': 'retrieve',
                                                                     'patch': 'partial_update'})),
    re_path(r'dev/gateway/$', GateWayView.as_view()),
]