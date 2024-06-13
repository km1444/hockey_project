from itertools import chain

from liga2_seasons_app.models import TeamInTable1gr, TeamInTable2gr


def all_team(request):
    all_team_liga2_1 = TeamInTable1gr.objects.values(
        'team_name__title',
        'team_name__city'
    ).order_by('team_name__title').distinct()
    all_team_liga2_2 = TeamInTable2gr.objects.values(
        'team_name__title',
        'team_name__city'
    ).order_by('team_name__title').distinct()
    all_team_liga2 = list(chain(all_team_liga2_1, all_team_liga2_2))
    result_all_teams = [
        dict(s) for s in set(frozenset(d.items()) for d in all_team_liga2)
    ]
    return {
        'all_team_liga2': result_all_teams
    }
