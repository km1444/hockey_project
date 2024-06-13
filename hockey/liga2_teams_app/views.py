# from django.contrib.auth.decorators import login_required
from itertools import chain

from django.shortcuts import get_object_or_404, render
# from .forms import (
#     AddTeamAdditionalTournamentForm, AddTeamForm,
#     AddTeamTransitionTournamentForm, CreateTeamForm,
#     EditTeamInAdditionalTournamentForm, EditTeamInBasicTournamentForm,
#     EditTeamInTransitionTournamentForm,
# )
from liga2_seasons_app.models import TeamInTable1gr, TeamInTable2gr
from rating.models import Team


def history_team(request, team):
    """ функция формирования содержимого страницы с историей команды """
    team_seasons_1 = TeamInTable1gr.objects.filter(
        team_name__title=team).select_related(
            'season',
            'transition_tournament',
            'additional_tournament',
            'additional_tournament_second',
            'transition_tournament_without_points').order_by('-season__name')
    team_seasons_2 = TeamInTable2gr.objects.filter(
        team_name__title=team).select_related(
            'season',
            'transition_tournament',
            'additional_tournament',
            'additional_tournament_second',
            'transition_tournament_without_points').order_by('-season__name')
    team_seasons = sorted(
        chain(team_seasons_1, team_seasons_2),
        key=lambda x: x.season.name, reverse=True
    )
    team = get_object_or_404(Team, title=team)
    count_season = team_seasons_1.count() + team_seasons_2.count()
    context = {
        'team_seasons': team_seasons,
        'team': team,
        'count_season': count_season,
    }
    template = 'liga2_teams/liga2_history_team.html'
    return render(request, template, context)
