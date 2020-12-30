from rest_framework.viewsets import ModelViewSet
from book_hero.models import BookInfo, HeroInfo
from .serializers import BookSerializer, HeroSerializer
from .tasks import debug_task, print_strftime
import logging
celery_logger = logging.getLogger('celery')


class BookViewSet(ModelViewSet):
    queryset = BookInfo.objects.all()
    serializer_class = BookSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs)

        # debug_task.delay()

        print_strftime.delay()

        return response


class HeroViewSet(ModelViewSet):
    queryset = HeroInfo.objects.all()
    serializer_class = HeroSerializer

