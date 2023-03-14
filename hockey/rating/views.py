import json

from django.core import serializers
from django.core.paginator import Paginator
from django.db.models import Sum
# from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Player, Statistic, Team_for_table


def index(request):
    total_points_for_players = Statistic.objects.values('name__name') \
        .annotate(game=Sum('game'), point=Sum('point')) \
        .order_by('-point', 'game')[:20]
    # print(total_points_for_players)
    # print(type(total_points_for_players))
    template = 'posts/index.html'
    context = {
        'page_obj': total_points_for_players,
        'table_name': 'Career Leaders for Points'
    }
    return render(request, template, context)


def team_players_in_season(request, team, season):
    team_statistic = Statistic.objects.filter(
        team__title=team, season__name=season
    )
    next_season = season[:2] + str(int((season)[2:4]) + 1) + \
        season[4:5] + str(int(season[5:]) + 1)
    previous_season = season[:2] + str(int((season)[2:4]) - 1) + \
        season[4:5] + str(int(season[5:]) - 1)
    template = 'posts/team_players_in_season.html'
    context = {
        'team': team,
        'season': season,
        'previous_season': previous_season,
        'next_season': next_season,
        'page_obj': team_statistic,
    }
    return render(request, template, context)


def player_detail(request, name):
    player = get_object_or_404(Player, name=name)
    player_seasons = player.statistics.all().order_by('season')
    count = player_seasons.count()
    game = sum(i.game for i in player_seasons)
    goal = sum(i.goal for i in player_seasons)
    assist = sum(i.assist for i in player_seasons)
    point = sum(i.point for i in player_seasons)
    penalty = sum(i.penalty for i in player_seasons)
    position = player_seasons[0].position
    template = 'posts/profile.html'
    context = {
        'player': player,
        'count': count,
        'page_obj': player_seasons,
        'game': game,
        'goal': goal,
        'assist': assist,
        'point': point,
        'penalty': penalty,
        'position': position
    }
    return render(request, template, context)


def best_of_season(request, season):
    next_season = season[:2] + str(int((season)[2:4]) + 1) + \
        season[4:5] + str(int(season[5:]) + 1)
    previous_season = season[:2] + str(int((season)[2:4]) - 1) + \
        season[4:5] + str(int(season[5:]) - 1)
    player_scores = Statistic.objects.all().filter(season__name=season)
    player_scores_2 = Statistic.objects.filter(season__name=season) \
        .values('name__name').annotate(
            team=Sum('team__title'),
            game=Sum('game'),
            goal=Sum('goal'),
            assist=Sum('assist'),
            point=Sum('point'),
            penalty=Sum('penalty')).order_by('-point', '-goal', 'game')[55:60]
    print(player_scores_2)
    # print(player_scores[0])
    # print(dir(player_scores[0].name))
    paginator = Paginator(player_scores, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = 'posts/best_of_season.html'
    context = {
        'season': season,
        'previous_season': previous_season,
        'next_season': next_season,
        'page_obj': page_obj
    }
    return render(request, template, context)


def all_time_all_player_one_team(request, team):
    total_points_for_players = Statistic.objects.all() \
        .filter(team__title=team) \
        .values('name__name') \
        .annotate(games=Sum('game'), points=Sum('point')) \
        .order_by('-points', 'games')[:50]
    # paginator = Paginator(total_points_for_players, 20)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    template = 'posts/all_time_all_player_one_team.html'
    context = {
        'page_obj': total_points_for_players,
        'team': team
    }
    return render(request, template, context)


def statistic(request, stat_rule):
    if stat_rule == 'goals_career':
        total_goals_for_players = Statistic.objects.all() \
            .values('name__name') \
            .annotate(game=Sum('game'), goal=Sum('goal')) \
            .order_by('-goal', 'game')[:20]
        context = {
            'page_obj': total_goals_for_players,
            'table_name': 'Career Leaders for Goals'
        }
    elif stat_rule == 'goals_season':
        total_goals_for_players = Statistic.objects \
            .values('name__name', 'season__name', 'game', 'goal') \
            .order_by('-goal', 'game')[:20]
        context = {
            'page_obj': total_goals_for_players,
            'table_name': 'Single Season Leaders for Goals'
        }
    elif stat_rule == 'assist_career':
        total_assist_for_players = Statistic.objects.all() \
            .values('name__name') \
            .annotate(game=Sum('game'), assist=Sum('assist')) \
            .order_by('-assist', 'game')[:20]
        context = {
            'page_obj': total_assist_for_players,
            'table_name': 'Career Leaders for Assist'
        }
    elif stat_rule == 'assist_season':
        total_assist_for_players = Statistic.objects \
            .values('name__name', 'season__name', 'game', 'assist') \
            .order_by('-assist', 'game')[:20]
        context = {
            'page_obj': total_assist_for_players,
            'table_name': 'Single Season Leaders for Assist'
        }
    elif stat_rule == 'point_season':
        total_point_for_players = Statistic.objects \
            .values('name__name', 'season__name', 'game', 'point') \
            .order_by('-point', 'game')[:20]
        context = {
            'page_obj': total_point_for_players,
            'table_name': 'Single Season Leaders for Points'
        }
    elif stat_rule == 'games_career':
        total_games_for_players = Statistic.objects.all() \
            .values('name__name') \
            .annotate(game=Sum('game')) \
            .order_by('-game')[:20]
        context = {
            'page_obj': total_games_for_players,
            'table_name': 'Career Leaders for Games'
        }
    elif stat_rule == 'penalty_career':
        total_penalty_for_players = Statistic.objects.all() \
            .values('name__name') \
            .annotate(game=Sum('game'), penalty=Sum('penalty')) \
            .order_by('-penalty', 'game')[:20]
        context = {
            'page_obj': total_penalty_for_players,
            'table_name': 'Career Leaders for Penalty'
        }
    elif stat_rule == 'penalty_season':
        total_penalty_for_players = Statistic.objects \
            .values('name__name', 'season__name', 'game', 'penalty') \
            .order_by('-penalty', 'game')[:20]
        context = {
            'page_obj': total_penalty_for_players,
            'table_name': 'Single Season Leaders for Penalty'
        }
    template = 'posts/index.html'
    return render(request, template, context)


def create_table(request, season):
    teams = Team_for_table.objects.all() \
        .filter(season__name=season).order_by('rank')
    next_season = season[:2] + str(int((season)[2:4]) + 1) + \
        season[4:5] + str(int(season[5:]) + 1)
    previous_season = season[:2] + str(int((season)[2:4]) - 1) + \
        season[4:5] + str(int(season[5:]) - 1)
    #####
    query_top_5 = Statistic.objects.all().filter(season__name=season)[:5]
    top_5 = serializers.serialize(
        "json",
        query_top_5,
        fields=("name", 'team', "point"),
        use_natural_foreign_keys=True
    )
    serialized_data_top_5 = json.loads(top_5)
    ####
    total_goals_for_players = Statistic.objects.all() \
        .filter(season__name=season).order_by('-goal', 'game')[:5]
    top_5_goal = serializers.serialize(
        "json",
        total_goals_for_players,
        fields=('name', 'team', 'goal'),
        use_natural_foreign_keys=True
    )
    serialized_data_top_5_goal = json.loads(top_5_goal)
    #####
    total_assist_for_players = Statistic.objects.all() \
        .filter(season__name=season).order_by('-assist', 'game')[:5]
    top_5_assist = serializers.serialize(
        "json",
        total_assist_for_players,
        fields=('name', 'team', 'assist'),
        use_natural_foreign_keys=True
    )
    serialized_data_top_5_assist = json.loads(top_5_assist)
    #####
    total_penalty_for_players = Statistic.objects.all() \
        .filter(season__name=season).order_by('-penalty', 'game')[:5]
    top_5_penalty = serializers.serialize(
        "json",
        total_penalty_for_players,
        fields=('name', 'team', 'penalty'),
        use_natural_foreign_keys=True
    )
    serialized_data_top_5_penalty = json.loads(top_5_penalty)
    #####
    template = 'table/teams_table.html'
    context = {
        'previous_season': previous_season,
        'next_season': next_season,
        'page_obj': teams,
        'season': season,
        'top_5': serialized_data_top_5,
        'top_5_goal': serialized_data_top_5_goal,
        'top_5_assist': serialized_data_top_5_assist,
        'top_5_penalty': serialized_data_top_5_penalty,
    }
    return render(request, template, context)
