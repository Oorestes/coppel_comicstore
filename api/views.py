import requests

from collections import namedtuple
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from comicstore.settings import MARVEL_ENDPOINT, MARVEL_LIMIT

from .functions import get_marvel_hash
from .serializers import CharacterSerializer, ComicSerializer, SearchingSerializer, UserModelSerializer, UserRegisterSerializer
from .models import Character, Comic

"""
searchComics
"""
@api_view(['GET'])
def all_characters(request):
    """
    Returns a list of all characters ordered by name.
    """

    # Parametros el request
    offset = 0
    params = {'orderBy': 'name', 'offset': offset, 'limit': MARVEL_LIMIT} | get_marvel_hash()

    """
    El ejercicio contemplaba traer todos los personajes de marvel. La parte comentada del codigo hace exactamente eso, pero debido
    al tiempo que toma extraer todos los datos, la limité a los primeros 100 siguiendo las condiciones de ordenamiento establecidas
    """

    characters = []
    # Iteramos la api hasta que no haya más records
    # while True:        
    #     response = requests.get(f"{MARVEL_ENDPOINT}/characters", params=params).json()
    #     response_body = response['data']['results']
    #
    #     for character in response_body:
    #         characters.append(Character(id=character['id'], name=character['name'], image=f"{character['thumbnail']['path']}.{character['thumbnail']['extension']}", appearances=character['comics']['available']))
    #
    #     offset += MARVEL_LIMIT
    #
    #     if body['count'] < MARVEL_LIMIT:
    #         break

    # Eliminar las siguientes dos lineas si se quiere iterar para traer todos los records.
    response = requests.get(f"{MARVEL_ENDPOINT}/characters", params=params).json()
    response_body = response['data']['results']
    
    for character in response_body:
        characters.append(Character(id=character['id'], name=character['name'], image=f"{character['thumbnail']['path']}.{character['thumbnail']['extension']}", appearances=character['comics']['available']))

    serializer = CharacterSerializer(characters, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def search_by_word(request, searchTerm):
    """
    Fetch all charactes and comics that match the search term provided.
    """

    # Parametros para los requests
    character_params = {'nameStartsWith': searchTerm} | get_marvel_hash()
    comic_params = {'format': 'comic', 'formatType': 'comic', 'noVariants': 'true', 'orderBy': 'title', 'titleStartsWith': searchTerm} | get_marvel_hash()

    characters = []
    comics = []

    character_response = requests.get(f"{MARVEL_ENDPOINT}/characters", params=character_params).json()
    character_response_body = character_response['data']['results']

    comic_response = requests.get(f"{MARVEL_ENDPOINT}/comics", params=comic_params).json()
    comic_response_body = comic_response['data']['results']

    for character in character_response_body:
        characters.append(Character(id=character['id'], name=character['name'], image=f"{character['thumbnail']['path']}.{character['thumbnail']['extension']}", appearances=character['comics']['available']))

    for comic in comic_response_body:
        comics.append(Comic(id=comic['id'], title=comic['title'], image=f"{comic['thumbnail']['path']}.{comic['thumbnail']['extension']}", onsaleDate=f"{comic['dates'][0]['date']}" ))
    
    Searching = namedtuple('Searching', ('characters', 'comics'))
    searches = Searching(characters=characters, comics=comics)
    serializer = SearchingSerializer(searches)

    return Response(serializer.data)


@api_view(['GET'])
def search_by_character(request, name):
    """
    Fetch all characters whose name matches with the provided name.
    """

    character_params = {'nameStartsWith': name} | get_marvel_hash()

    character_response = requests.get(f"{MARVEL_ENDPOINT}/characters", params=character_params).json()
    character_response_body = character_response['data']['results']

    characters = []
    for character in character_response_body:
        characters.append(Character(id=character['id'], name=character['name'], image=f"{character['thumbnail']['path']}.{character['thumbnail']['extension']}", appearances=character['comics']['available']))

    character_serializer = CharacterSerializer(characters, many=True)

    return Response(character_serializer.data)


@api_view(['GET'])
def search_by_comic(request, title):
    """
    Fetch all comics whose name matches with the provided name.
    """

    comic_params = {'format': 'comic', 'formatType': 'comic', 'noVariants': 'true', 'orderBy': 'title', 'titleStartsWith': title} | get_marvel_hash()

    comic_response = requests.get(f"{MARVEL_ENDPOINT}/comics", params=comic_params).json()
    comic_response_body = comic_response['data']['results']

    comics = []
    for comic in comic_response_body:
        comics.append(Comic(id=comic['id'], title=comic['title'], image=f"{comic['thumbnail']['path']}.{comic['thumbnail']['extension']}", onsaleDate=f"{comic['dates'][0]['date']}" ))

    comic_serializer = ComicSerializer(comics, many=True)
    return Response(comic_serializer.data)


"""
users
"""
@api_view(['GET'])
def all_users(request):
    """
    Fetch all users displaying not sensitive data such as: id, username, date joined.
    """

    serializer = UserModelSerializer(User.objects.all(), many=True)
    return Response(serializer.data)


@api_view(['POST'])
def register_user(request):
    """
    Register new unique user.
    Expects a JSON object {"username": "string", "password", "string"} in body request.
    """

    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        if user:
            return Response(status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def authenticate_user(request):
    """
    Authenticates a user based on the username and password provided.
    If the provided credentials are correct it returns an authorization token.
    Expect a JSON object {"username": "string", "password", "string"} in body request.
    """

    user = authenticate(request, username=request.data['username'], password=request.data['password'])
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_account(request, format=None):
    """
    Assuming you are already authenticated and retrieved your token from '/users/authenticate', providing
    your token as auth method will return your user information.
    Expect Token on request 'Token ???????????????????????????'
    """
    user = User.objects.get(username=str(request.user))
    response = {
        'id': user.id,
        'user': user.username,
        'date_joined': user.date_joined,
        'token': str(request.auth),
    }
    return Response(response)


"""
addToLayaway
"""