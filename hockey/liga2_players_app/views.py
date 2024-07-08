import operator

from functools import reduce

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Max, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views.generic.edit import UpdateView
from goalkeeper_liga2_app.models import GoalkeeperStatisticLiga2
from liga2_seasons_app.models import TeamInTable1gr, TeamInTable2gr
from rating.forms import AddPlayerForm
from rating.models import Season, Team
from rating.secondary import prev_next_season

from .forms import AddStatisticLiga2Form, EditStatisticLiga2Form
from .models import StatisticPlayer


def index(request):
    """Лидеры по голам во всей первой лиге за все время"""
    total_points_for_players = StatisticPlayer.objects.values(
        'name__id', 'name__name').annotate(
            game=Sum('game'),
            goal=Sum('goal')).order_by(
                '-goal', 'game')[:100]
    paginator = Paginator(total_points_for_players, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    start_index = page_obj.start_index() - 1
    template = 'liga2_seasons/liga2_index.html'
    context = {
        'page_obj': page_obj,
        'start_index': start_index,
        'table_name': 'Most Goals Career League 1',
        'title': 'Лучшие бомбардиры советского хоккея в первой лиге'
    }
    return render(request, template, context)


def player_statistics_in_the_league1(request, stat_rule):
    rule = stat_rule.split('_')
    if rule[1] == 'career':
        total_for_players = StatisticPlayer.objects.values(
            'name__id',
            'name__name'
        ).annotate(
            game=Sum('game'),
            goal=Sum('goal'),
            assist=Sum('assist'),
            point=Sum('point'),
            penalty=Sum('penalty')
        ).order_by(
            f'-{rule[0]}',
            'game'
        )[:100]
        paginator = Paginator(total_for_players, 25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        start_index = page_obj.start_index() - 1
        context = {
            'page_obj': page_obj,
            'start_index': start_index,
            'table_name':
            'Most ' + f'{rule[0].title()}''s' + ' Career League 1',
        }
    elif rule[1] == 'season':
        total_for_players = StatisticPlayer.objects.values(
            'name__id',
            'name__name',
            'season__name'
        ).annotate(
            game=Sum('game'),
            goal=Sum('goal'),
            assist=Sum('assist'),
            point=Sum('point'),
            penalty=Sum('penalty')
        ).order_by(
            f'-{rule[0]}',
            'game'
        )[:100]
        paginator = Paginator(total_for_players, 25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        start_index = page_obj.start_index() - 1
        context = {
            'page_obj': page_obj,
            'start_index': start_index,
            'table_name':
            'Most ' + f'{rule[0].title()}''s' + ' Single Season League 1'
        }
    elif rule[1] == 'yearly':
        best_goals = StatisticPlayer.objects.values(
            'season__name'
        ).annotate(
            goal=Max('goal'))
        q_object = reduce(operator.or_, (Q(**x) for x in best_goals))
        queryset = StatisticPlayer.objects.values(
            'name__id',
            'name__name',
            'season__name',
            'goal',
            'game'
        ).filter(q_object).order_by('season__name')
        paginator = Paginator(queryset, 25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        start_index = page_obj.start_index() - 1
        context = {
            'page_obj': page_obj,
            'start_index': start_index,
            'table_name':
            'Yearly Leaders for ' + f'{rule[0].title()}''s League 1'
        }
    template = 'liga2_seasons/liga2_index.html'
    return render(request, template, context)


def players_team_season(request, team, season):
    """Отображение страницы со статистикой игроков по команде и сезону"""
    team_get = get_object_or_404(Team, title=team)
    info_of_team = TeamInTable1gr.objects.filter(
        team_name__title=team, season__name=season)
    info_of_team_2gr = TeamInTable2gr.objects.filter(
        team_name__title=team, season__name=season)
    season_get = get_object_or_404(Season, name=season)
    team_statistic = StatisticPlayer.objects.filter(
        team__title=team, season__name=season
    ).values(
        'id',
        'name',
        'name__name',
        'age',
        'game',
        'goal',
        'assist',
        'point',
        'penalty'
    ).order_by('-point', '-goal', 'game')
    goalkeepers = GoalkeeperStatisticLiga2.objects.filter(
        team__title=team, season__name=season).values(
        'id',
        'name',
        'name__name',
        'age',
        'game',
        'goal_against',
        'penalty'
    ).order_by('-game')
    context = {
        'page_obj': team_statistic,
        'season': season_get,
        'team': team_get,
        'info_of_team': info_of_team,
        'info_of_team_2gr': info_of_team_2gr,
        'previous_season': prev_next_season(season)[1],
        'next_season': prev_next_season(season)[0],
        'goalkeepers': goalkeepers,
    }
    template = 'liga2_players/liga2_players_team_season.html'
    return render(request, template, context)


def leaders_goals_season(request, season):
    """Лидеры по голам в сезоне. Статистика игроков в сезоне - голы"""
    leaders_goals_season = StatisticPlayer.objects.filter(
        season__name=season
    ).values(
        'name__id', 'name__name', 'age', 'team__slug').annotate(
            game=Sum('game'),
            value=Sum('goal')).order_by(
                '-goal', 'game')[:20]
    context = {
        'players_list': leaders_goals_season,
        'season': season,
        'title_table': 'Goals leaders',
        'column_heading': 'G',
        'previous_season': prev_next_season(season)[1],
        'next_season': prev_next_season(season)[0],
        'link': 'liga2_players:leaders_goals_season'
    }
    template = 'liga2_players/liga2_statistical_leaders_of_the_season.html'
    return render(request, template, context)


def leaders_assists_season(request, season):
    """Лидеры по передачам в сезоне. Статистика игроков в сезоне - передачи"""
    leaders_assists_season = StatisticPlayer.objects.filter(
        season__name=season
    ).values(
        'name__id', 'name__name', 'age', 'team__slug').annotate(
            game=Sum('game'),
            value=Sum('assist')).order_by(
                '-assist', 'game')[:20]
    context = {
        'players_list': leaders_assists_season,
        'season': season,
        'title_table': 'Assists leaders',
        'column_heading': 'A',
        'previous_season': prev_next_season(season)[1],
        'next_season': prev_next_season(season)[0],
        'link': 'liga2_players:leaders_assists_season'
    }
    template = 'liga2_players/liga2_statistical_leaders_of_the_season.html'
    return render(request, template, context)


def leaders_points_season(request, season):
    """Лидеры по очкам в сезоне. Статистика игроков в сезоне - очки"""
    leaders_points_season = StatisticPlayer.objects.filter(
        season__name=season
    ).values(
        'name__id', 'name__name', 'age', 'team__slug').annotate(
            game=Sum('game'),
            value=Sum('point')).order_by(
                '-point', 'game')[:20]
    context = {
        'players_list': leaders_points_season,
        'season': season,
        'title_table': 'Points leaders',
        'column_heading': 'PTS',
        'previous_season': prev_next_season(season)[1],
        'next_season': prev_next_season(season)[0],
        'link': 'liga2_players:leaders_points_season'
    }
    template = 'liga2_players/liga2_statistical_leaders_of_the_season.html'
    return render(request, template, context)


def leaders_penaltys_season(request, season):
    """Лидеры по штрафу в сезоне. Статистика игроков в сезоне - штраф"""
    leaders_penaltys_season = StatisticPlayer.objects.filter(
        season__name=season
    ).values(
        'name__id', 'name__name', 'age', 'team__slug').annotate(
            game=Sum('game'),
            value=Sum('penalty')).order_by(
                '-penalty', 'game')[:20]
    context = {
        'players_list': leaders_penaltys_season,
        'season': season,
        'title_table': 'Penalty leaders',
        'column_heading': 'PIM',
        'previous_season': prev_next_season(season)[1],
        'next_season': prev_next_season(season)[0],
        'link': 'liga2_players:leaders_penaltys_season'
    }
    template = 'liga2_players/liga2_statistical_leaders_of_the_season.html'
    return render(request, template, context)


@login_required
def add_statistic_liga2(request, team, season):
    """Функция добавления статистической записи об игроке,
    с автозаполнением полей с названием команды и сезона"""
    form = AddStatisticLiga2Form(team, season, request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('liga2_players:players_team_season', team, season)
    form = AddStatisticLiga2Form(team, season)
    context = {
        'form': form,
        'team': team,
        'season': season
    }
    return render(request, 'forms/liga2/liga2_create_statistic.html', context)


@login_required
def add_player_liga2(request, team, season):
    """Добавление игрока в базу"""
    form = AddPlayerForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(
            'liga2_players:create_statistic_liga2', team, season)
    form = AddPlayerForm()
    return render(request, 'forms/create_player.html', {'form': form})


class SkaterStatisticLiga2UpdateView(UpdateView):
    form_class = EditStatisticLiga2Form
    pk_url_kwarg = 'id'
    template_name = "forms/liga2/liga2_create_statistic.html"

    def get_queryset(self):
        return StatisticPlayer.objects.filter(
            id=self.kwargs['id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team'] = self.kwargs['team']
        context['season'] = self.kwargs['season']
        return context

    def get_success_url(self, **kwargs):
        return reverse(
            'liga2_players:players_team_season',
            kwargs={
                'team': self.kwargs['team'], 'season': self.kwargs['season']
            },
        )
