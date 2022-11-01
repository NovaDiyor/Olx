from rest_framework import serializers
from rest_framework import serializers
from main.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "all"


class AdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ads
        fields = "all"
