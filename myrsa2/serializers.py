from rest_framework import serializers

from myrsa2.models import App


class KeymanagerSerializer(serializers.ModelSerializer):
    enterprise = serializers.StringRelatedField()
    plat_pri_key = serializers.CharField(write_only=True)

    class Meta:
        model = App
        fields = "__all__"

