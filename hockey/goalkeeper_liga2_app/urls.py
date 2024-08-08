from django.urls import path

from . import views

app_name = 'goalkeeper_liga2'

urlpatterns = [
    path(
        'add_goalkeeper_statistic_liga2/<str:team>/<str:season>',
        # views.add_goalkeeper_statistic_liga2,
        views.AddKeeperStatLiga2.as_view(),
        name='add_goalkeeper_statistic_liga2'
    ),
    path(
        'add_player_goalkeeper/<str:team>/<str:season>',
        # views.add_player_goalkeeper,
        views.AddPlayerGoalkeeper.as_view(),
        name='add_player_goalkeeper'
    ),
    path(
        'edit_goalkeeper_stat_liga2/<str:team>/<str:season>/<int:id>',
        views.EditGoalkeeperStatLiga2.as_view(),
        name='edit_goalkeeper_stat_liga2'
    ),
    path(
        'delete_goalkeeper_stat_liga2/<str:team>/<str:season>/<int:id>',
        views.DeleteGoalkeeperStatLiga2.as_view(),
        name='delete_goalkeeper_stat_liga2'
    ),
    path(
        'goalkeepers_in_the_first_league/',
        # views.goalkeepers_in_the_first_league,
        views.ListGoalkeepersLiga2.as_view(),
        name='goalkeepers_in_the_first_league'
    ),
]
