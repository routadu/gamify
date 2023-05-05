from rest_framework import serializers
from .models import User, GameProgress


class UserProfileDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)


class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class UserAuthDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'name', 'email', 'age')


class GameProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameProgress
        fields = ('username', 'gameID', 'level')
