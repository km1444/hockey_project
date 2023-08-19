from django.db.models import Sum
from django.shortcuts import get_object_or_404
from rating.models import Player, Statistic, Team, TeamForTable
from rest_framework import generics

from .serializers import (
    PlayerSerializer, StatisticSerializer, TeamForTableSerializer,
    TeamSerializer,
)


class PlayerList(generics.ListAPIView):
    """Получение списка игроков с суммированием игр и очков, сортировка"""
    serializer_class = PlayerSerializer

    def get_queryset(self):
        return Player.objects.values('name').annotate(
            total_game=Sum('statistics__game'),
            total_point=Sum('statistics__point')
        ).order_by('-total_point')[:10]


class PlayerDetail(generics.ListAPIView):
    """Статистика выступлений одного игрока"""
    serializer_class = StatisticSerializer

    def get_queryset(self):
        player = get_object_or_404(Player, id=self.kwargs.get('id'))
        return player.statistics.all().order_by('-season')


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
