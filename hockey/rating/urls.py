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
    path('player/<str:name>/', views.player_detail, name='player_detail'),
    path('year/<str:season>', views.best_of_season, name='best_of_season'),
    path(
        'team/<str:team>',
        views.all_time_all_player_one_team,
        name='all_time_all_player_one_team'
    ),
    path('players/<str:stat_rule>/', views.statistic, name='goals_career'),
    path('players/<str:stat_rule>/', views.statistic, name='goal_season'),
    path('players/<str:stat_rule>/', views.statistic, name='assist_career'),
    path('players/<str:stat_rule>/', views.statistic, name='assist_season'),
    path('players/<str:stat_rule>/', views.statistic, name='point_season'),
    path('players/<str:stat_rule>/', views.statistic, name='games_career'),
    path('players/<str:stat_rule>/', views.statistic, name='penalty_season'),
    path('players/<str:stat_rule>/', views.statistic, name='penalty_career'),
    path('table/<str:season>/', views.create_table, name='create_table')
]
