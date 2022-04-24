from django.urls import path

from .views import all_characters, all_users, authenticate_user, register_user, search_by_character, search_by_comic, search_by_word, user_account


urlpatterns = [
    # searchComics
    path('searchComics/', all_characters),
    path('searchComics/<str:searchTerm>/search', search_by_word),
    path('searchComics/<str:name>/character', search_by_character),
    path('searchComics/<str:title>/comic', search_by_comic),

    # users
    path('users/', all_users),
    path('users/register', register_user),
    path('users/authenticate', authenticate_user),
    path('users/account', user_account),

    # addToLayaway

    # getLayawayList/
]
