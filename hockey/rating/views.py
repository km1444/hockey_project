from django.core.paginator import Paginator
from django.db.models import Sum
# from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Player, Statistic


def index(request):
    total_points_for_players = Statistic.objects.all().values('name__name') \
        .annotate(game=Sum('game'), point=Sum('point')) \
        .order_by('-point', 'game')[:20]
    # paginator = Paginator(total_points_for_players, 20)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
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


# def most_assist(request):
#     total_assist_for_players = Statistic.objects.all() \
#         .values('name__name') \
#         .annotate(game=Sum('game'), assist=Sum('assist')) \
#         .order_by('-assist', 'game')[:20]
#     template = 'posts/index.html'
#     context = {
#         'page_obj': total_assist_for_players,
#         'table_name': 'Career Leaders for Assist'
#     }
#     print(context)
#     return render(request, template, context)


# def assist(request, assist):
#     if assist == 'assist_career':
#         total_assist_for_players = Statistic.objects.all() \
#             .values('name__name') \
#             .annotate(game=Sum('game'), assist=Sum('assist')) \
#             .order_by('-assist', 'game')[:20]
#         context = {
#             'page_obj': total_assist_for_players,
#             'table_name': 'Career Leaders for Assist'
#         }
#     else:
#         # goals == 'goals_season':
#         total_assist_for_players = Statistic.objects \
#             .values('name__name', 'season__name', 'game', 'assist') \
#             .order_by('-assist', 'game')[:20]
#         context = {
#             'page_obj': total_assist_for_players,
#             'table_name': 'Single Season Leaders for Assist'
#         }
#     template = 'posts/index.html'
#     return render(request, template, context)
