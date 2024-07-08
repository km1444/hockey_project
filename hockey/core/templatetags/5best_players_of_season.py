from django import template
from django.db.models import Sum
from liga2_players_app.models import StatisticPlayer

register = template.Library()


@register.inclusion_tag("liga2_players/top_5_players_liga2.html")
def top_5_players(season):
    top_5_point = StatisticPlayer.objects.filter(
        season__name=season).values(
            'name__id',
            'name__name',
            'team__slug').annotate(
                game=Sum('game'),
                point=Sum('point')).order_by(
                    '-point',
                    'game')[:5]
    top_5_goal = StatisticPlayer.objects.filter(
        season__name=season).values(
            'name__id',
            'name__name',
            'team__slug').annotate(
                game=Sum('game'),
                goal=Sum('goal')).order_by(
                    '-goal',
                    'game')[:5]
    top_5_assist = StatisticPlayer.objects.filter(
        season__name=season).values(
            'name__id',
            'name__name',
            'team__slug').annotate(
                game=Sum('game'),
                assist=Sum('assist')).order_by(
                    '-assist',
                    'game')[:5]
    top_5_penalty = StatisticPlayer.objects.filter(
        season__name=season).values(
            'name__id',
            'name__name',
            'team__slug').annotate(
                game=Sum('game'),
                penalty=Sum('penalty')).order_by(
                    '-penalty',
                    'game')[:5]
    context = {
        'top_5_point': top_5_point,
        'top_5_goal': top_5_goal,
        'top_5_assist': top_5_assist,
        'top_5_penalty': top_5_penalty,
        'season': season,
    }
    return context
