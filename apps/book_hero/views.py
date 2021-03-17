from rest_framework.viewsets import ModelViewSet
from book_hero.models import BookInfo, HeroInfo
from .serializers import BookSerializer, HeroSerializer
import logging
celery_logger = logging.getLogger('celery')


class BookViewSet(ModelViewSet):
    queryset = BookInfo.objects.all()
    serializer_class = BookSerializer


class HeroViewSet(ModelViewSet):
    queryset = HeroInfo.objects.all()
    serializer_class = HeroSerializer

