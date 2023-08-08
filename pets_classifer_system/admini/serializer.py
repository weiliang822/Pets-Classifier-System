from rest_framework import serializers

from django.contrib.auth.models import User
from .models import Model, Photo


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class PhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'


class ModelsSerializer(serializers.ModelSerializer):
    photos = PhotosSerializer(many=True)

    class Meta:
        model = Model
        fields = '__all__'
