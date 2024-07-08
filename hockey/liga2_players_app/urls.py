from django.urls import path

from . import views
from .views import SkaterStatisticLiga2UpdateView

app_name = 'liga2_players'

urlpatterns = [
    path(
        'most_goals_career/',
        views.index,
        name='liga2_most_goals_career'
    ),
    path(
        'player_statistics_in_the_league1/<str:stat_rule>',
        views.player_statistics_in_the_league1,
        name='player_statistics_in_the_league1'
    ),
    path(
        '<str:team>/<str:season>/',
        views.players_team_season,
        name='players_team_season'
    ),
    path(
        'create_statistic_liga2/<str:team>/<str:season>',
        views.add_statistic_liga2,
        name='create_statistic_liga2'
    ),
    path(
        'create_player_liga2/<str:team>/<str:season>',
        views.add_player_liga2,
        name='create_player_liga2'
    ),
    path(
        'edit_skater_statistic_liga2/<str:team>/<str:season>/<int:id>',
        SkaterStatisticLiga2UpdateView.as_view(),
        name='edit_skater_statistic_liga2'
    ),
    path(
        'leaders_goals/<str:season>',
        views.leaders_goals_season,
        name='leaders_goals_season'
    ),
    path(
        'leaders_assists/<str:season>',
        views.leaders_assists_season,
        name='leaders_assists_season'
    ),
    path(
        'leaders_points/<str:season>',
        views.leaders_points_season,
        name='leaders_points_season'
    ),
    path(
        'leaders_penaltys/<str:season>',
        views.leaders_penaltys_season,
        name='leaders_penaltys_season'
    )
]
