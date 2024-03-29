from rest_framework import serializers
from .models import User
from django.utils import timezone


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'pseudo', 'password', 'profile_image', 'token_refresh']
        extra_kwargs= {
            'password': {'write_only': True}
        }  

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        pseudo = validated_data.pop('pseudo', None)
        if password is not None:
            instance.set_password(password)
        if pseudo is not None:
            instance.pseudo = pseudo
        instance.save()
        return instance
