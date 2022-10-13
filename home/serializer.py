from rest_framework import serializers
from .models import HomeSliderMoudel,HomeContainersModel

class HomeSliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeSliderMoudel
        fields = ('id','description','name','img_x_large')

class HomeContainersSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeContainersModel
        fields = ('id','description','name','img_x_large')