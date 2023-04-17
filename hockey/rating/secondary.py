from django.db.models import Sum

from .models import Statistic


def top_goal(team):
    top = Statistic.objects.filter(
        team__title=team).values('name__id', 'name__name') \
        .annotate(goal=Sum('goal')) \
        .order_by('-goal')[:1]
    return top[0]


def top_point(team):
    top = Statistic.objects.filter(
        team__title=team).values('name__id', 'name__name') \
        .annotate(point=Sum('point')) \
        .order_by('-point')[:1]
    return top[0]


def top_season_goal(team):
    top_s_goal = Statistic.objects.filter(
        team__title=team).values(
            'name__id', 'name__name', 'goal', 'season__name') \
        .order_by('-goal')[:1]
    return top_s_goal[0]
    

def top_season_point(team):
    top_s_point = Statistic.objects.filter(
        team__title=team).values(
            'name__id', 'name__name', 'point', 'season__name') \
        .order_by('-point')[:1]
    return top_s_point[0]


def prev_next_season(season):
    next_season = season[:2] + str(int((season)[2:4]) + 1) + \
        season[4:5] + str(int(season[5:]) + 1)
    previous_season = season[:2] + str(int((season)[2:4]) - 1) + \
        season[4:5] + str(int(season[5:]) - 1)
    return (next_season, previous_season)
