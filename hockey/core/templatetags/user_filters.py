from django import template
from coach_app.models import CoachStatistic
from django.db.models import Sum
from goalkeeper_liga2_app.models import GoalkeeperStatisticLiga2
# from django.shortcuts import get_object_or_404
from liga2_players_app.models import StatisticPlayer

# from rating.models import Player

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.inclusion_tag("liga2_players/player_detail_of_liga2.html")
def show_player_detail_of_liga2(id):
    seasons_of_player = StatisticPlayer.objects.filter(name=id).values(
        'name',
        'name__name',
        'age',
        'team__title',
        'season__name',
        'game',
        'goal',
        'assist',
        'point',
        'penalty',
        'position__name'
    ).order_by('season__name')
    game = sum(i['game'] for i in seasons_of_player)
    goal = sum(i['goal'] for i in seasons_of_player)
    assist = sum(i['assist'] for i in seasons_of_player)
    point = sum(i['point'] for i in seasons_of_player)
    penalty = sum(i['penalty'] for i in seasons_of_player)
    amount_teams = seasons_of_player.values('team__title').distinct().count()
    group_teams = seasons_of_player.values('team__title').annotate(
        game=Sum('game'),
        goal=Sum('goal'),
        assist=Sum('assist'),
        point=Sum('point'),
        penalty=Sum('penalty')
    ).order_by('-game')
    count = seasons_of_player.values('season').distinct().count()
    position = seasons_of_player[0]['position__name']
    context = {
        'count': count,
        'seasons_of_player': seasons_of_player,
        'game': game,
        'goal': goal,
        'assist': assist,
        'point': point,
        'penalty': penalty,
        'group_teams': group_teams,
        'amount_teams': amount_teams,
        'position': position,
    }
    return context


@register.inclusion_tag("coach/show_coach_stat_of_player.html")
def show_coach_stat_of_player(id):
    coach_obj = CoachStatistic.objects.filter(coach_name=id).values(
        'coach_name',
        'coach_name__name',
        'age',
        'team__title',
        'season__name',
        'final_position',
        'full_season',
        'fired_season',
        'came_season'
    ).order_by('season__name')
    context = {
        'coach_obj': coach_obj,
    }
    return context


@register.inclusion_tag("liga2_players/goalkeeper_detail_of_liga2.html")
def show_goalkeeper_detail_of_liga2(id):
    goalkeeper_seasons = GoalkeeperStatisticLiga2.objects.filter(
        name=id).values(
            'name',
            'name__name',
            'age',
            'team__title',
            'season__name',
            'game',
            'goal_against',
            'penalty'
    ).order_by('season__name')
    game = sum(i['game'] for i in goalkeeper_seasons)
    goal_against = sum(i['goal_against'] for i in goalkeeper_seasons)
    penalty = sum(i['penalty'] for i in goalkeeper_seasons)
    amount_teams = goalkeeper_seasons.values(
        'team__title').distinct().count()
    group_teams = goalkeeper_seasons.values('team__title').annotate(
        game=Sum('game'),
        goal_against=Sum('goal_against'),
        penalty=Sum('penalty')
    ).order_by('-game')
    count = goalkeeper_seasons.values('season').distinct().count()
    position = 'Вратарь'
    context = {
        'count': count,
        'page_obj': goalkeeper_seasons,
        'game': game,
        'goal_against': goal_against,
        'penalty': penalty,
        'position': position,
        'group_teams': group_teams,
        'amount_teams': amount_teams,
    }
    return context
