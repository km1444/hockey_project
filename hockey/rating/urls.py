from django.urls import path

from . import views

app_name = 'rating'

urlpatterns = [
    path('', views.index, name='index'),
    path(
        'team/<str:team>/<str:season>/',
        views.team_players_in_season,
        name='team_players_in_season'
    ),
    path(
        'leaders/<str:team>/',
        views.leaders_career,
        name='leaders_career'
    ),
    path(
        'season_leaders/<str:team>/',
        views.season_leaders,
        name='season_leaders'
    ),
    path('player/<int:id>/', views.player_detail, name='player_detail'),
    path('players/<str:stat_rule>/', views.statistic, name='statistic'),
    path(
        'year/<str:season>/<str:stat_rule>/',
        views.best_of_season,
        name='best_of_season'
    ),
    path(
        'team/<str:team>/',
        views.all_time_all_player_one_team,
        name='all_time_all_player_one_team'
    ),
    path('table/<str:season>/', views.create_table, name='create_table'),
    path('history/<str:team>/', views.history_team, name='history_team')
]
