from rest_framework import serializers
from rest_framework import serializers
from main.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class AdsSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Ads
        fields = "__all__"


class Add_Ads_Seria(serializers.ModelSerializer):
    class Meta:
        model = Ads
        fields = "__all__"


class SubSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Subcategory
        fields = "__all__"


class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Information
        fields = "__all__"
