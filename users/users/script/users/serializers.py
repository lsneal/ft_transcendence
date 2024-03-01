from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'pseudo', 'password', 'victory', 'nb_game']
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
    
    #def update():
    #    https://stackoverflow.com/questions/46061406/how-to-update-user-data-using-django-and-rest-framework
    
