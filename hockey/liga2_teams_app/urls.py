from django.urls import path

from . import views

app_name = 'liga2_teams'

urlpatterns = [
    path('history/<str:team>/', views.history_team, name='history_team'),
    path(
        'season_leaders/<str:team>/',
        views.season_leaders,
        name='season_leaders'
    ),
    path(
        'career_leaders/<str:team>/',
        views.career_leaders,
        name='career_leaders'
    ),
    path(
        'all_players_on_team/<str:team>/',
        views.all_players_on_team,
        name='all_players_on_team'
    ),
    path(
        'first_league_team_goalkeepers/<str:team>/',
        views.first_league_team_goalkeepers,
        name='first_league_team_goalkeepers'
    ),
]
