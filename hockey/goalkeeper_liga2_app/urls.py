from django.urls import path

from . import views

app_name = 'goalkeeper_liga2'

urlpatterns = [
    path(
        'add_goalkeeper_statistic_liga2/<str:team>/<str:season>',
        views.add_goalkeeper_statistic_liga2,
        name='add_goalkeeper_statistic_liga2'
    ),
    path(
        'add_player_goalkeeper/<str:team>/<str:season>',
        views.add_player_goalkeeper,
        name='add_player_goalkeeper'
    ),
    # path(
    #     'edit_goalkeeper_statistic_liga2/<str:team>/<str:season>/<int:id>',
    #     views.edit_goalkeeper_statistic_liga2,
    #     name='edit_goalkeeper_statistic_liga2'
    # ),
    path(
        'goalkeepers_in_the_first_league/',
        views.goalkeepers_in_the_first_league,
        name='goalkeepers_in_the_first_league'
    ),
]
