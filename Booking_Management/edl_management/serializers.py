from django.contrib.auth.models import User, Group
from .models import *
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'email')

class UserProfileInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('contact', 'photo_profile', 'tel', 'faculty', 'branch', 'photo_profile',)
