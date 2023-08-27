from django.urls import path
from rating.views import (
    GoalkeeperStatisticListView, SearchResultsView, SkaterStatisticDeleteView,
    SkaterStatisticUpdateView,
)

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
    path(
        'goalkeepers/<str:team>/',
        views.goalie_list_team,
        name='goalie_list_team'
    ),
    path('table/<str:season>/', views.create_table, name='create_table'),
    path('history/<str:team>/', views.history_team, name='history_team'),
    path('search/', SearchResultsView.as_view(), name='search_result'),
    path(
        'goalkeeper/<int:pk>/',
        GoalkeeperStatisticListView.as_view(),
        name='goalkeeper_detail'
    ),
    path(
        'create_statistic/<str:team>/<str:season>',
        views.add_statistic,
        name='create_statistic'
    ),
    path(
        'create_player/<str:team>/<str:season>',
        views.add_player,
        name='create_player'
    ),
    path(
        'create_goalkeeper_statistic/<str:team>/<str:season>',
        views.add_goalkeeper_statistic,
        name='create_goalkeeper_statistic'
    ),
    path(
        'create_player_goalkeeper/<str:team>/<str:season>',
        views.add_player_goalkeeper,
        name='create_player_goalkeeper'
    ),
    path(
        'edit_skater_statistic/<str:team>/<str:season>/<int:id>',
        # views.edit_skater_statistic,
        SkaterStatisticUpdateView.as_view(),
        name='edit_skater_statistic'
    ),
    path(
        'delete_skater_statistic/<str:team>/<str:season>/<int:id>',
        SkaterStatisticDeleteView.as_view(),
        name='delete_skater_statistic'
    ),
    path(
        'edit_goalkeeper_statistic/<str:team>/<str:season>/<int:id>',
        views.edit_goalkeeper_statistic,
        name='edit_goalkeeper_statistic'
    ),
    path(
        'delete_goalkeeper_statistic/<str:team>/<str:season>/<int:id>',
        views.delete_goalkeeper_statistic,
        name='delete_goalkeeper_statistic'
    ),
]
