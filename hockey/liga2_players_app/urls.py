from django.urls import path

from . import views

# from .views import Index, SkaterStatisticLiga2UpdateView

app_name = 'liga2_players'

urlpatterns = [
    # path(
    #     'most_goals_career/',
    #     views.Index.as_view(),
    #     name='liga2_most_goals_career'
    # ),
    path(
        'player_statistics_in_the_league1/<str:stat_rule>',
        # views.player_statistics_in_the_league1,
        views.PlayerStatisticsByCategory.as_view(),
        name='player_statistics_in_the_league1'
    ),
    path(
        '<str:team>/<str:season>/',
        # views.players_team_season,
        views.PlayersTeamSeason.as_view(),
        name='players_team_season'
    ),
    path(
        'create_statistic_liga2/<str:team>/<str:season>',
        # views.add_statistic_liga2,
        views.AddStatisticLiga2.as_view(),
        name='create_statistic_liga2'
    ),
    path(
        'create_player_liga2/<str:team>/<str:season>',
        # views.add_player_liga2,
        views.AddPlayerLiga2.as_view(),
        name='create_player_liga2'
    ),
    path(
        'edit_skater_statistic_liga2/<str:team>/<str:season>/<int:id>',
        views.SkaterStatisticLiga2UpdateView.as_view(),
        name='edit_skater_statistic_liga2'
    ),
    path(
        'delete_skater_stat_liga2/<str:team>/<str:season>/<int:id>',
        views.DeleteSkaterStatLiga2DeleteView.as_view(),
        name='delete_skater_stat_liga2'
    ),
    path(
        'leaders_goals/<str:season>',
        # views.leaders_goals_season,
        views.LeadersGoalsSeason.as_view(),
        name='leaders_goals_season'
    ),
    path(
        'leaders_assists/<str:season>',
        # views.leaders_assists_season,
        views.LeadersAssistsSeason.as_view(),
        name='leaders_assists_season'
    ),
    path(
        'leaders_points/<str:season>',
        # views.leaders_points_season,
        views.LeadersPointsSeason.as_view(),
        name='leaders_points_season'
    ),
    path(
        'leaders_penaltys/<str:season>',
        # views.leaders_penaltys_season,
        views.LeadersPenaltysSeason.as_view(),
        name='leaders_penaltys_season'
    )
]
