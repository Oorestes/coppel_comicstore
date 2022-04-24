from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, Serializer

from .models import Character, Comic


class CharacterSerializer(ModelSerializer):
    class Meta:
        model = Character
        fields = ('id', 'name', 'image', 'appearances')


class ComicSerializer(ModelSerializer):
    class Meta:
        model = Comic
        fields = ('id', 'title', 'image', 'onsaleDate')


class SearchingSerializer(Serializer):
    characters = CharacterSerializer(many=True)
    comics = ComicSerializer(many=True)


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username','date_joined', 'is_active')


class UserRegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password')

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['password'])
        user.set_password(validated_data['password']) # Cambiamos el comportamiento para que la contraseña se guarde cifrada y no como texto plano
        user.save()
        return user
