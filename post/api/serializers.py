from rest_framework import serializers
from post.models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    uploader = UserSerializer()

    class Meta:
        model = Post
        fields = '__all__'
