from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = 'UserSerializer'
        model = User
        fields = ('id', 'username')
