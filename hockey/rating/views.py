# from aggregates import StringAgg
# from django.core.paginator import Paginator
# from django.db import models
from django.db.models import Sum
from django.shortcuts import get_object_or_404, render

from .models import Player, Statistic, Team_for_table
from .secondary import (
    prev_next_season, top_goal, top_point, top_season_goal, top_season_point,
)


def index(request):
    total_points_for_players = Statistic.objects.values(
        'name__id', 'name__name') \
        .annotate(game=Sum('game'), point=Sum('point')) \
        .order_by('-point', 'game')[:20]
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


def player_detail(request, id):
    player = get_object_or_404(Player, id=id)
    player_seasons = player.statistics.order_by('season')
    print(type(player_seasons))
    count = player_seasons.values('season').distinct().count()
    game = sum(i.game for i in player_seasons)
    goal = sum(i.goal for i in player_seasons)
    assist = sum(i.assist for i in player_seasons)
    point = sum(i.point for i in player_seasons)
    penalty = sum(i.penalty for i in player_seasons)
    amount_teams = player_seasons.values('team__title').distinct().count()
    group_teams = player_seasons.values('team__title').annotate(
        game=Sum('game'),
        goal=Sum('goal'),
        assist=Sum('assist'),
        point=Sum('point'),
        penalty=Sum('penalty')
    ).order_by('-game')
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
        'position': position,
        'group_teams': group_teams,
        'amount_teams': amount_teams,
    }
    return render(request, template, context)


def best_of_season(request, season, stat_rule):
    # queryset_season = Statistic.objects.filter(season__name=season)
    if stat_rule == 'goal':
        player_scores = Statistic.objects.filter(
            season__name=season).order_by('-goal', 'game', '-point')[:20]
    if stat_rule == 'assist':
        player_scores = Statistic.objects.filter(season__name=season).order_by(
            '-assist', 'game', '-point')[:20]
    if stat_rule == 'point':
        player_scores = Statistic.objects.filter(
            season__name=season).order_by('-point', '-goal', 'game')[:20]
    if stat_rule == 'penalty':
        player_scores = Statistic.objects.filter(
            season__name=season).order_by('-penalty', 'game', )[:20]
    template = 'posts/best_of_season.html'
    context = {
        'season': season,
        'previous_season': prev_next_season(season)[1],
        'next_season': prev_next_season(season)[0],
        'page_obj': player_scores,
        # 'page_obj_all': player_scores_all,
        'stat_rule': stat_rule
    }
    return render(request, template, context)


def all_time_all_player_one_team(request, team):
    total_points_for_players = Statistic.objects.all() \
        .filter(team__title=team) \
        .values('name__id', 'name__name') \
        .annotate(
            games=Sum('game'), goals=Sum('goal'), assists=Sum('assist'),
            points=Sum('point'), penalty=Sum('penalty')).order_by(
        '-points', '-goals', 'games')
    # total_points_for_players_20 = total_points_for_players
    # total_points_for_players_all = total_points_for_players[20:]
    template = 'posts/all_time_all_player_one_team.html'
    context = {
        'page_obj': total_points_for_players,
        'team': team,
        'top_goal': top_goal(team),
        'top_point': top_point(team),
        'top_s_goal': top_season_goal(team),
        'top_s_point': top_season_point(team),
    }
    return render(request, template, context)


def statistic(request, stat_rule):
    if stat_rule == 'goals_career':
        total_goals_for_players = Statistic.objects.all() \
            .values('name__id', 'name__name') \
            .annotate(game=Sum('game'), goal=Sum('goal')) \
            .order_by('-goal', 'game')[:20]
        context = {
            'page_obj': total_goals_for_players,
            'table_name': 'Career Leaders for Goals'
        }
    elif stat_rule == 'goals_season':
        total_goals_for_players = Statistic.objects \
            .values('name__id', 'name__name', 'season__name', 'game', 'goal') \
            .order_by('-goal', 'game')[:20]
        context = {
            'page_obj': total_goals_for_players,
            'table_name': 'Single Season Leaders for Goals'
        }
    elif stat_rule == 'assist_career':
        total_assist_for_players = Statistic.objects.all() \
            .values('name__id', 'name__name') \
            .annotate(game=Sum('game'), assist=Sum('assist')) \
            .order_by('-assist', 'game')[:20]
        context = {
            'page_obj': total_assist_for_players,
            'table_name': 'Career Leaders for Assist'
        }
    elif stat_rule == 'assist_season':
        total_assist_for_players = Statistic.objects \
            .values(
                'name__id', 'name__name', 'season__name', 'game', 'assist') \
            .order_by('-assist', 'game')[:20]
        context = {
            'page_obj': total_assist_for_players,
            'table_name': 'Single Season Leaders for Assist'
        }
    elif stat_rule == 'point_season':
        total_point_for_players = Statistic.objects \
            .values(
                'name__id', 'name__name', 'season__name', 'game', 'point') \
            .order_by('-point', 'game')[:20]
        context = {
            'page_obj': total_point_for_players,
            'table_name': 'Single Season Leaders for Points'
        }
    elif stat_rule == 'games_career':
        total_games_for_players = Statistic.objects.all() \
            .values('name__id', 'name__name') \
            .annotate(game=Sum('game')) \
            .order_by('-game')[:20]
        context = {
            'page_obj': total_games_for_players,
            'table_name': 'Career Leaders for Games'
        }
    elif stat_rule == 'penalty_career':
        total_penalty_for_players = Statistic.objects.all() \
            .values('name__id', 'name__name') \
            .annotate(game=Sum('game'), penalty=Sum('penalty')) \
            .order_by('-penalty', 'game')[:20]
        context = {
            'page_obj': total_penalty_for_players,
            'table_name': 'Career Leaders for Penalty'
        }
    elif stat_rule == 'penalty_season':
        total_penalty_for_players = Statistic.objects \
            .values(
                'name__id', 'name__name', 'season__name', 'game', 'penalty') \
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
    query_top_5_1 = Statistic.objects.filter(
        season__name=season).values('name__id', 'name__name', 'team__slug') \
        .annotate(game=Sum('game'), point=Sum('point')) \
        .order_by('-point', 'game')[:5]
    # print(query_top_5_1)
    # top_5 = serializers.serialize(
    #     "json",
    #     query_top_5,
    #     fields=("name", 'team', "point"),
    #     use_natural_foreign_keys=True
    # )
    # serialized_data_top_5 = json.loads(top_5)
    ####
    top_5_goal = Statistic.objects.filter(
        season__name=season).values('name__id', 'name__name', 'team__slug') \
        .annotate(game=Sum('game'), goal=Sum('goal')) \
        .order_by('-goal', 'game')[:5]
    #####
    top_5_assist = Statistic.objects.filter(
        season__name=season).values('name__id', 'name__name', 'team__slug') \
        .annotate(game=Sum('game'), assist=Sum('assist')) \
        .order_by('-assist', 'game')[:5]
    #####
    top_5_penalty = Statistic.objects.filter(
        season__name=season).values('name__id', 'name__name', 'team__slug') \
        .annotate(game=Sum('game'), penalty=Sum('penalty')) \
        .order_by('-penalty', 'game')[:5]
    #####
    template = 'table/teams_table.html'
    context = {
        'previous_season': previous_season,
        'next_season': next_season,
        'page_obj': teams,
        'season': season,
        'top_5': query_top_5_1,
        'top_5_goal': top_5_goal,
        'top_5_assist': top_5_assist,
        'top_5_penalty': top_5_penalty,
    }
    return render(request, template, context)


def leaders_career(request, team):
    top_10_game = Statistic.objects.filter(
        team__title=team).values('name__id', 'name__name') \
        .annotate(game=Sum('game')) \
        .order_by('-game')[:10]
    top_10_goal = Statistic.objects.filter(
        team__title=team).values('name__id', 'name__name') \
        .annotate(goal=Sum('goal')) \
        .order_by('-goal')[:10]
    top_10_assist = Statistic.objects.filter(
        team__title=team).values('name__id', 'name__name') \
        .annotate(assist=Sum('assist')) \
        .order_by('-assist')[:10]
    top_10_penalty = Statistic.objects.filter(
        team__title=team).values('name__id', 'name__name') \
        .annotate(penalty=Sum('penalty')) \
        .order_by('-penalty')[:10]
    # top_goal(team)
    context = {
        'top_10_game': top_10_game,
        'top_10_goal': top_10_goal,
        'top_10_assist': top_10_assist,
        'top_10_penalty': top_10_penalty,
        'team': team,
        'top_goal': top_goal(team),
        'top_point': top_point(team),
        'top_s_goal': top_season_goal(team),
        'top_s_point': top_season_point(team)
    }
    template = 'posts/leaders_career.html'
    return render(request, template, context)


def season_leaders(request, team):
    top_10_goal = Statistic.objects.filter(
        team__title=team).values(
            'name__id', 'name__name', 'goal', 'season__name') \
        .order_by('-goal')[:10]
    top_10_assist = Statistic.objects.filter(
        team__title=team).values(
        'name__id', 'name__name', 'assist', 'season__name') \
        .order_by('-assist')[:10]
    top_10_point = Statistic.objects.filter(
        team__title=team).values(
        'name__id', 'name__name', 'point', 'season__name') \
        .order_by('-point')[:10]
    top_10_penalty = Statistic.objects.filter(
        team__title=team).values(
        'name__id', 'name__name', 'penalty', 'season__name') \
        .order_by('-penalty')[:10]
    context = {
        'top_10_goal': top_10_goal,
        'top_10_assist': top_10_assist,
        'top_10_point': top_10_point,
        'top_10_penalty': top_10_penalty,
        'team': team,
        'top_goal': top_goal(team),
        'top_point': top_point(team),
        'top_s_goal': top_season_goal(team),
        'top_s_point': top_season_point(team)
    }
    template = 'posts/season_leaders.html'
    return render(request, template, context)


def history_team(request, team):
    team_view = Team_for_table.objects.filter(
        name__title=team).order_by('-season')
    count_season = team_view.count()
    context = {
        'team_view': team_view,
        'team': team,
        'count_season': count_season,
        'top_goal': top_goal(team),
        'top_point': top_point(team),
        'top_s_goal': top_season_goal(team),
        'top_s_point': top_season_point(team)
    }
    template = 'posts/history_team.html'
    return render(request, template, context)
