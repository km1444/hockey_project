from django.db.models import Sum
from django.shortcuts import get_object_or_404
from rating.models import Player, Statistic, Team, TeamForTable
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import (
    PlayerMostGoalsSerializer, PlayerSerializer, StatisticSerializer,
    TeamForTableSerializer, TeamSerializer,
)

# class PlayerList(generics.ListAPIView):
#     """Получение списка игроков с суммированием игр и очков, сортировка"""
#     serializer_class = PlayerSerializer

#     def get_queryset(self):
#         data = Statistic.objects.values(
#             'name__name').annotate(
#                 game=Sum('game'), point=Sum('point')).order_by(
#                     '-point', 'game')[:20]
#         return data


@api_view(['GET'])
def player_list(request):
    player_points = Statistic.objects.values(
        'name__id', 'name__name').annotate(
            game=Sum('game'), point=Sum('point')).order_by(
                '-point', 'game')[:20]
    serializer = PlayerSerializer(player_points, many=True)
    return Response(serializer.data)


class PlayerMostGoalsList(generics.ListAPIView):
    serializer_class = PlayerMostGoalsSerializer

    def get_queryset(self):
        data = Statistic.objects.values(
            'name__name').annotate(
                game=Sum('game'), goal=Sum('goal')).order_by(
                    '-goal', 'game')[:10]
        return data


class PlayerDetail(generics.ListAPIView):
    """Статистика выступлений одного игрока"""
    serializer_class = StatisticSerializer

    def get_queryset(self):
        player = get_object_or_404(Player, id=self.kwargs.get('id'))
        return player.statistics.all().order_by('season__name')


class PlayerListTeamSeason(generics.ListAPIView):
    """Список игроков одной команды в определенный сезон"""
    serializer_class = StatisticSerializer

    def get_queryset(self):
        return Statistic.objects.filter(
            team__title=self.kwargs.get('team'),
            season__name=self.kwargs.get('season')
        )


class TeamList(generics.ListCreateAPIView):
    """список всех команд"""
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamHistory(generics.ListAPIView):
    """Список сезонов одной команды"""
    serializer_class = TeamForTableSerializer

    def get_queryset(self):
        return TeamForTable.objects.filter(
            name__title=self.kwargs.get('team')).order_by('season__name')


class SeasonLeadersTeam(generics.ListAPIView):
    """Лучшие результаты по очкам за сезон в истории клуба"""
    serializer_class = StatisticSerializer

    def get_queryset(self):
        team = get_object_or_404(Team, title=self.kwargs.get('team'))
        queryset_top = team.statistics.all()
        # top_10_point = queryset_top.order_by('-point')[:2]
        top_10_goal = queryset_top.order_by('-goal')[:2]
        return top_10_goal
