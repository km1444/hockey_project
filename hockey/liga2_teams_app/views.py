# from django.contrib.auth.decorators import login_required
from itertools import chain

from django.db.models import Sum
from django.shortcuts import get_object_or_404, render
from goalkeeper_liga2_app.models import GoalkeeperStatisticLiga2
from liga2_players_app.models import StatisticPlayer
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
            'transition_tournament_without_points',
            'additional_tournament_without_points').order_by('-season__name')
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
        # 'header_team_season': show_leaders_team_season(team),
        # 'header_team_career': show_leaders_team_career(team)
    }
    template = 'liga2_teams/liga2_history_team.html'
    return render(request, template, context)


def show_leaders_team_season(team):
    query_list = StatisticPlayer.objects.filter(
        team__title=team).values(
            'name__id',
            'name__name',
            'season__name',
            'goal',
            'assist',
            'point',
            'penalty')
    header_team_players_season = {
        'top_s_goal': query_list.order_by('-goal')[:1][0],
        'top_s_point': query_list.order_by('-point')[:1][0],
    }
    return header_team_players_season


def show_leaders_team_career(team):
    query_list = StatisticPlayer.objects.filter(
        team__title=team).values(
            'name__id',
            'name__name').annotate(
                goal=Sum('goal'),
                point=Sum('point'))
    header_team_players_career = {
        'top_goal': query_list.order_by('-goal')[:1][0],
        'top_point': query_list.order_by('-point')[:1][0],
    }
    return header_team_players_career


def season_leaders(request, team):
    team = get_object_or_404(Team, title=team)
    query_list = StatisticPlayer.objects.filter(
        team__title=team).values(
            'name__id',
            'name__name',
            'season__name',
            'goal',
            'assist',
            'point',
            'penalty')
    top_10_goal = query_list.order_by('-goal')[:10]
    top_10_assist = query_list.order_by('-assist')[:10]
    top_10_point = query_list.order_by('-point')[:10]
    top_10_penalty = query_list.order_by('-penalty')[:10]
    context = {
        'top_10_goal': top_10_goal,
        'top_10_assist': top_10_assist,
        'top_10_point': top_10_point,
        'top_10_penalty': top_10_penalty,
        'team': team,
        # 'header_team_season': show_leaders_team_season(team),
        # 'header_team_career': show_leaders_team_career(team)
    }
    template = 'liga2_teams/liga2_season_leaders.html'
    return render(request, template, context)


def career_leaders(request, team):
    """Десятка лучших по основным показателям за карьеру
    в команде"""
    team = get_object_or_404(Team, title=team)
    query_list = StatisticPlayer.objects.filter(
        team__title=team).values(
            'name__id',
            'name__name').annotate(
                game=Sum('game'),
                goal=Sum('goal'),
                assist=Sum('assist'),
                point=Sum('point'),
                penalty=Sum('penalty')
    )
    goalkeeper_list = GoalkeeperStatisticLiga2.objects.filter(
        team__title=team).values(
            'name__id',
            'name__name').annotate(
                game=Sum('game')
    ).order_by('-game')[:10]
    top_10_game = query_list.order_by('-game')[:10]
    top_10_goal = query_list.order_by('-goal', 'game')[:10]
    top_10_assist = query_list.order_by('-assist', 'game')[:10]
    top_10_point = query_list.order_by('-point', '-goal')[:10]
    top_10_penalty = query_list.order_by('-penalty', 'game')[:10]
    context = {
        'top_10_game': top_10_game,
        'top_10_goal': top_10_goal,
        'top_10_assist': top_10_assist,
        'top_10_point': top_10_point,
        'goalkeeper_list': goalkeeper_list,
        'top_10_penalty': top_10_penalty,
        'team': team,
        # 'header_team_season': show_leaders_team_season(team),
        # 'header_team_career': show_leaders_team_career(team)
    }
    template = 'liga2_teams/liga2_career_leaders.html'
    return render(request, template, context)


def all_players_on_team(request, team):
    team = get_object_or_404(Team, title=team)
    total_points_for_players = StatisticPlayer.objects.filter(
        team__title=team).values(
            'name__id', 'name__name').annotate(
                games=Sum('game'),
                goals=Sum('goal'),
                assists=Sum('assist'),
                points=Sum('point'),
                penalty=Sum('penalty')).order_by(
                    '-points', '-goals', 'games')
    template = 'liga2_teams/liga2_all_players_on_team.html'
    context = {
        'page_obj': total_points_for_players,
        'team': team,
        # 'header_team_season': show_leaders_team_season(team),
        # 'header_team_career': show_leaders_team_career(team)
    }
    return render(request, template, context)


def first_league_team_goalkeepers(request, team):
    team = get_object_or_404(Team, title=team)
    goalkeeper_list = GoalkeeperStatisticLiga2.objects.filter(
        team__title=team).values(
            'name__id', 'name__name').annotate(
                games=Sum('game'),
                goals=Sum('goal_against'),
                penalty=Sum('penalty')).order_by('-games')
    template = 'liga2_teams/liga2_team_goalkeepers.html'
    context = {
        'page_obj': goalkeeper_list,
        'team': team,
        # 'header_team_season': show_leaders_team_season(team),
        # 'header_team_career': show_leaders_team_career(team)
        'title': 'Вратари каманды первой лиги'
    }
    return render(request, template, context)
