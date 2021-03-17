from . import models
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BookInfo
        fields = "__all__"


class HeroSerializer(serializers.ModelSerializer):
    hbook = serializers.StringRelatedField()

    class Meta:
        model = models.HeroInfo
        fields = "__all__"
