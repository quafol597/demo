from django.urls import re_path

from book_hero.views import BookViewSet, HeroViewSet

app_name = 'book_hero'

urlpatterns = [
    re_path(r'^books/$', BookViewSet.as_view({'get': 'list',
                                             'post': 'create',
                                             'delete': 'destroy',
                                             'put': 'update'}), name='books'),
    re_path(r'^books/(?P<pk>\d+)/$', BookViewSet.as_view({'get': 'retrieve',
                                                         'patch': 'partial_update'})),
    re_path(r'^hero/$', HeroViewSet.as_view({'get': 'list',
                                             'post': 'create',
                                             'delete': 'destroy',
                                             'put': 'update'})),
    re_path(r'^hero/(?P<pk>\d+)/$', HeroViewSet.as_view({'get': 'retrieve',
                                                         'patch': 'partial_update'})),

]