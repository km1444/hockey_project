import operator

from functools import reduce
from itertools import chain

from coach_app.models import CoachStatistic
from django.contrib import messages  # type: ignore
from django.contrib.auth.decorators import login_required  # type: ignore
from django.core.paginator import Paginator
from django.db.models import Max, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views.decorators.cache import cache_page
from django.views.generic import ListView
from django.views.generic.edit import DeleteView, UpdateView
# from goalkeeper_app.views import GoalkeeperStatisticListView
from goalkeeper_liga2_app.models import GoalkeeperStatisticLiga2
from liga2_players_app.models import StatisticPlayer

from .forms import (
    AddGoalkeeperStatisticForm, AddPlayerForm, AddStatisticForm,
    EditGoalkeeperStatisticForm, EditStatisticForm,
)
from .models import (
    DescriptionTable, GoalkeeperStatistic, PersonPlayoff, Player, Playoff,
    Season, Statistic, Team, TeamForTable, TeamForTable2, TeamForTable2Round,
    TeamForTable2Round2, TeamForTable2Round3, TeamForTable3, TeamForTable4,
)
from .secondary import (
    all_team_league_one, prev_next_season, top_goal, top_point,
    top_season_goal, top_season_point,
)


def index(request):
    total_points_for_players = Statistic.objects.values(
        'name__id', 'name__name').annotate(
            game=Sum('game'),
            goal=Sum('goal')).order_by(
                '-goal', 'game').filter(goal__gte=100)
    paginator = Paginator(total_points_for_players, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    start_index = page_obj.start_index() - 1
    template = 'posts/index.html'
    context = {
        'page_obj': page_obj,
        'start_index': start_index,
        # 'table_name': 'Career Leaders for Goals',
        'table_name': 'Most Goals Career',
        'table_description':
        'Лидеры по голам за карьеру в высшей лиге советского хоккея',
        'title': 'Лидеры по голам за карьеру в высшей лиге советского хоккея'
    }
    return render(request, template, context)


def team_players_in_season(request, team, season):
    team = get_object_or_404(Team, title=team)
    season = get_object_or_404(Season, name=season)
    team_statistic = Statistic.objects.filter(
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
    goalkeepers = GoalkeeperStatistic.objects.filter(
        team__title=team, season__name=season
    ).values(
        'id',
        'name',
        'name__name',
        'age',
        'game',
        'goal_against',
        'penalty'
    ).order_by('-game')
    coaches = CoachStatistic.objects.filter(
        team__title=team, season__name=season
    ).values(
        'id',
        'coach_name',
        'coach_name__name'
    )
    team_info = TeamForTable.objects.filter(
        name__title=team.title,
        season__name=season.name
    ).values('current_name', 'name__title', 'name__city')
    team_info_2 = TeamForTable2.objects.filter(
        name__title=team.title,
        season__name=season.name
    ).values('current_name', 'name__title', 'name__city')
    team_info_3 = TeamForTable3.objects.filter(
        name__title=team.title,
        season__name=season.name
    ).values('current_name', 'name__title', 'name__city')
    team_info_4 = TeamForTable4.objects.filter(
        name__title=team.title,
        season__name=season.name
    ).values('current_name', 'name__title', 'name__city')
    template = 'posts/team_players_in_season.html'
    context = {
        'team': team,
        'team_info': team_info,
        'team_info_2': team_info_2,
        'team_info_3': team_info_3,
        'team_info_4': team_info_4,
        'season': season,
        'previous_season': prev_next_season(season.name)[1],
        'next_season': prev_next_season(season.name)[0],
        'page_obj': team_statistic,
        'goalkeepers': goalkeepers,
        'coaches': coaches,
    }
    return render(request, template, context)


def player_detail(request, id):
    context = {}
    position = ''
    player = get_object_or_404(Player, id=id)
    player_seasons = player.statistics.values(
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
    goalkeeper_seasons = player.goalkeeperstatistic.values(
        'name',
        'name__name',
        'age',
        'team__title',
        'season__name',
        'game',
        'goal_against',
        'penalty'
    ).order_by('season__name')
    if player_seasons:
        game = sum(i['game'] for i in player_seasons)
        goal = sum(i['goal'] for i in player_seasons)
        assist = sum(i['assist'] for i in player_seasons)
        point = sum(i['point'] for i in player_seasons)
        penalty = sum(i['penalty'] for i in player_seasons)
        amount_teams = player_seasons.values('team__title').distinct().count()
        group_teams = player_seasons.values('team__title').annotate(
            game=Sum('game'),
            goal=Sum('goal'),
            assist=Sum('assist'),
            point=Sum('point'),
            penalty=Sum('penalty')
        ).order_by('-game')
        count = player_seasons.values('season').distinct().count()
        position = player_seasons[0]['position__name']
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
            'exist_statistic_of_major_league': True,
        }
    elif goalkeeper_seasons or GoalkeeperStatisticLiga2.objects.filter(
            name=id).exists():
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
        template = 'posts/profile_golie.html'
        context = {
            'player': player,
            'count': count,
            'page_obj': goalkeeper_seasons,
            'game': game,
            'goal_against': goal_against,
            'penalty': penalty,
            'position': position,
            'group_teams': group_teams,
            'amount_teams': amount_teams,
            'goalkeeper': True,
            'exist_statistic_goalkeeper_of_league1': True
        }
    else:
        context = {
            'player': player,
        }
        template = 'posts/profile.html'
    if StatisticPlayer.objects.filter(name=id).exists():
        context['exist_statistic_of_league1'] = True
        if not position:
            context['position'] = (
                StatisticPlayer.objects.filter(name=id).values(
                    'position__name')[0]['position__name'])
    if CoachStatistic.objects.filter(coach_name=id).exists():
        context['exist_coach_stat'] = True
    return render(request, template, context)


def best_of_season(request, season, stat_rule):
    player_scores = Statistic.objects.filter(
        season__name=season).values(
            'name__id', 'name__name', 'age', 'team__slug').annotate(
                game=Sum('game'),
                goal=Sum('goal'),
                assist=Sum('assist'),
                point=Sum('point'),
                penalty=Sum('penalty')).order_by(
                    f'-{stat_rule}', '-goal', 'game')[:20]
    template = 'posts/best_of_season.html'
    context = {
        'season': season,
        'previous_season': prev_next_season(season)[1],
        'next_season': prev_next_season(season)[0],
        'page_obj': player_scores,
        'stat_rule': stat_rule
    }
    return render(request, template, context)


def all_time_all_player_one_team(request, team):
    team = get_object_or_404(Team, title=team)
    total_points_for_players = Statistic.objects.filter(
        team__title=team).values(
            'name__id', 'name__name').annotate(
                games=Sum('game'),
                goals=Sum('goal'),
                assists=Sum('assist'),
                points=Sum('point'),
                penalty=Sum('penalty')).order_by(
                    '-points', '-goals', 'games')
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


def goalie_list_team(request, team):
    team = get_object_or_404(Team, title=team)
    total_goalkeeper = GoalkeeperStatistic.objects.filter(
        team__title=team).values(
            'name__id', 'name__name').annotate(
                games=Sum('game'),
                goals=Sum('goal_against'),
                penalty=Sum('penalty')).order_by('-games')
    template = 'posts/goalie_list_team.html'
    context = {
        'page_obj': total_goalkeeper,
        'team': team,
        'top_goal': top_goal(team),
        'top_point': top_point(team),
        'top_s_goal': top_season_goal(team),
        'top_s_point': top_season_point(team),
        'title': 'Вратари каманды'
    }
    return render(request, template, context)


def statistic(request, stat_rule):
    rule = stat_rule.split('_')
    dict_rule = {
        'goal': 'голам',
        'assist': 'передачам',
        'point': 'очкам',
        'penalty': 'штрафным минутам',
        'game': 'матчам'
    }
    if rule[1] == 'career':
        total_for_players = Statistic.objects.values(
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
            'Most ' + f'{rule[0].title()}''s' + ' Career',
            'table_description': (
                'Лидеры по '
                + f'{dict_rule[rule[0]]}'
                + ' за карьеру в высшей лиге советского хоккея'
            ),
            'title': (
                'Лидеры по '
                + f'{dict_rule[rule[0]]}'
                + ' за карьеру в высшей лиге советского хоккея'
            )
        }
    elif rule[1] == 'season':
        total_for_players = Statistic.objects.values(
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
            'Most ' + f'{rule[0].title()}''s' + ' Single Season',
            'table_description': (
                'Лидеры по '
                + f'{dict_rule[rule[0]]}'
                + ' за сезон в высшей лиге советского хоккея'
            ),
            'title': (
                'Лидеры по '
                + f'{dict_rule[rule[0]]}'
                + ' за сезон в высшей лиге советского хоккея'
            )
        }
    elif rule[1] == 'yearly':
        yearly_dict = {
            'goal': 'Приз "Лучший снайпер"',
            'assist': 'Лучший ассистент',
            'point': 'Приз "Самому результативному игроку"',
            'penalty': 'Самый грубый игрок сезона'
        }

        def yearly_func(val):
            if val == 'goal':
                return Statistic.objects.values(
                    'season__name').annotate(
                        goal=Max(val))
            if val == 'assist':
                return Statistic.objects.values(
                    'season__name').annotate(
                        assist=Max(val)).filter(
                            season__name__gte='1970-71')
            if val == 'point':
                return Statistic.objects.values(
                    'season__name').annotate(
                        point=Max(val))
        q_object = reduce(operator.or_, (Q(**x) for x in yearly_func(rule[0])))
        queryset = Statistic.objects.values(
            'name__id',
            'name__name',
            'season__name',
            'goal',
            'assist',
            'point',
            'penalty',
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
            'Yearly Leaders for ' + f'{rule[0].title()}''s',
            'table_description': yearly_dict[rule[0]]
        }
    template = 'posts/index.html'
    return render(request, template, context)


def create_table(request, season):
    # teams = TeamForTable.objects.filter(season__name=season).values(
    #     'id', 'rank', 'name__title', 'season__name', 'current_name',
    #     'games', 'wins', 'ties', 'losses', 'points').order_by('rank')
    teams = TeamForTable.objects.filter(
        season__name=season).select_related('name').order_by('rank')
    teams2 = TeamForTable2.objects.filter(
        season__name=season).select_related('name').order_by('rank')
    teams3 = TeamForTable3.objects.filter(
        season__name=season).select_related('name').order_by('rank')
    teams4 = TeamForTable4.objects.filter(
        season__name=season).select_related('name').order_by('rank')
    teams2round = TeamForTable2Round.objects.filter(
        season__name=season).select_related('name').order_by('rank')
    teams2round2 = TeamForTable2Round2.objects.filter(
        season__name=season).select_related('name').order_by('rank')
    teams2round3 = TeamForTable2Round3.objects.filter(
        season__name=season).select_related('name').order_by('rank')
    playoff = Playoff.objects.filter(season__name=season).values(
        'id', 'study', 'result_serie', 'team_1__title', 'team_2__title',
        'season__name', 'current_name_team_1', 'current_name_team_2'
    ).order_by('number')
    try:
        description_table = DescriptionTable.objects.get(season__name=season)
    except DescriptionTable.DoesNotExist:
        description_table = ''
    query_top_5_1 = Statistic.objects.filter(
        season__name=season).values(
            'name__id',
            'name__name',
            'team__slug').annotate(
                game=Sum('game'),
                point=Sum('point')).order_by(
                    '-point',
                    'game')[:5]
    top_5_goal = Statistic.objects.filter(
        season__name=season).values(
            'name__id',
            'name__name',
            'team__slug').annotate(
                game=Sum('game'),
                goal=Sum('goal')).order_by(
                    '-goal',
                    'game')[:5]
    top_5_assist = Statistic.objects.filter(
        season__name=season).values(
            'name__id',
            'name__name',
            'team__slug').annotate(
                game=Sum('game'),
                assist=Sum('assist')).order_by(
                    '-assist',
                    'game')[:5]
    top_5_penalty = Statistic.objects.filter(
        season__name=season).values(
            'name__id',
            'name__name',
            'team__slug').annotate(
                game=Sum('game'),
                penalty=Sum('penalty')).order_by(
                    '-penalty',
                    'game')[:5]
    template = 'table/teams_table.html'
    context = {
        'previous_season': prev_next_season(season)[1],
        'next_season': prev_next_season(season)[0],
        'page_obj': teams,
        'teams2': teams2,
        'teams3': teams3,
        'teams4': teams4,
        'teams2round': teams2round,
        'teams2round2': teams2round2,
        'teams2round3': teams2round3,
        'playoff': playoff,
        'description_table': description_table,
        'season': season,
        'top_5': query_top_5_1,
        'top_5_goal': top_5_goal,
        'top_5_assist': top_5_assist,
        'top_5_penalty': top_5_penalty,
    }
    return render(request, template, context)


def leaders_career(request, team):
    """Десятка лучших по основным показателям за карьеру
    в команде"""
    team = get_object_or_404(Team, title=team)
    query_list = Statistic.objects.filter(
        team__title=team).values(
            'name__id',
            'name__name').annotate(
                game=Sum('game'),
                goal=Sum('goal'),
                assist=Sum('assist'),
                point=Sum('point'),
                penalty=Sum('penalty')
    )
    goalkeeper_list = GoalkeeperStatistic.objects.filter(
        team__title=team).values(
            'name__id',
            'name__name').annotate(
                game=Sum('game')
    ).order_by('-game')[:10]
    top_10_game = query_list.order_by('-game')[:10]
    top_10_goal = query_list.order_by('-goal')[:10]
    top_10_assist = query_list.order_by('-assist')[:10]
    top_10_point = query_list.order_by('-point')[:10]
    top_10_penalty = query_list.order_by('-penalty')[:10]
    context = {
        'top_10_game': top_10_game,
        'top_10_goal': top_10_goal,
        'top_10_assist': top_10_assist,
        'top_10_point': top_10_point,
        'goalkeeper_list': goalkeeper_list,
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
    team = get_object_or_404(Team, title=team)
    query_list = Statistic.objects.filter(
        team__title=team).values(
            'name__id',
            'name__name',
            'season__name').annotate(
                goal=Sum('goal'),
                assist=Sum('assist'),
                point=Sum('point'),
                penalty=Sum('penalty'))
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
        'top_goal': top_goal(team),
        'top_point': top_point(team),
        'top_s_goal': top_season_goal(team),
        'top_s_point': top_season_point(team)
    }
    template = 'posts/season_leaders.html'
    return render(request, template, context)


@cache_page(60 * 15)
def history_team(request, team):
    """ функция формирования содержимого страницы с историей команды """
    team_view = TeamForTable.objects.filter(
        name__title=team).select_related(
            'season',
            'playoff',
            'coach_1',
            'coach_2',
            'coach_3').order_by('-season__name')
    team_view_2 = TeamForTable2.objects.filter(
        name__title=team).select_related(
            'season', 'coach_1',
            'coach_2',
            'coach_3').order_by('-season__name')
    team_view_3 = TeamForTable3.objects.filter(
        name__title=team).select_related(
            'season', 'coach_1',
            'coach_2',
            'coach_3').order_by('-season__name')
    team_view_4 = TeamForTable4.objects.filter(
        name__title=team).select_related(
            'season', 'coach_1',
            'coach_2',
            'coach_3').order_by('-season__name')
    round2_table1 = TeamForTable2Round.objects.filter(
        name__title=team).select_related('season').order_by('-season__name')
    round2_table2 = TeamForTable2Round2.objects.filter(
        name__title=team).select_related('season').order_by('-season__name')
    round2_table3 = TeamForTable2Round3.objects.filter(
        name__title=team).select_related('season').order_by('-season__name')
    result_playoff = PersonPlayoff.objects.filter(
        team__title=team).select_related('season').order_by('-season__name')
    team_view_general = sorted(
        chain(
            team_view, team_view_2, team_view_3, team_view_4, round2_table1,
            round2_table2, round2_table3, result_playoff),
        key=lambda x: x.season.name, reverse=True
    )
    team = get_object_or_404(Team, title=team)
    count_season = (
        (
            team_view.count() + team_view_2.count()
        ) + (team_view_3.count() + team_view_4.count())
    )
    if count_season == 1:
        end_word = ''
    elif count_season in [2, 3, 4]:
        end_word = 'а'
    else:
        end_word = 'ов'
    present_in_league_one = False
    if str(team) in list(all_team_league_one.keys()):
        present_in_league_one = True
    context = {
        'team_view_general': team_view_general,
        'team': team,
        'count_season': count_season,
        'end_word': end_word,
        'top_goal': top_goal(team),
        'top_point': top_point(team),
        'top_s_goal': top_season_goal(team),
        'top_s_point': top_season_point(team),
        'present_in_league_one': present_in_league_one,
    }
    template = 'posts/history_team.html'
    return render(request, template, context)


class SearchResultsView(ListView):
    model = Player
    template_name = 'search/search_result.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Player.objects.filter(
            Q(name__icontains=query.title()) | Q(
                year_of_birth__icontains=query)
        ).order_by('name')


@login_required
def add_statistic(request, team, season):
    """Функция добавления статистической записи об игроке,
    с автозаполнением полей с названием команды и сезона"""
    form = AddStatisticForm(team, season, request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('rating:team_players_in_season', team, season)
    form = AddStatisticForm(team, season)
    context = {
        'form': form,
        'team': team,
        'season': season
    }
    return render(request, 'forms/create_statistic.html', context)


@login_required
def add_player(request, team, season):
    """Добавление игрока в базу"""
    form = AddPlayerForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(
            'rating:create_statistic', team, season)
    form = AddPlayerForm()
    return render(request, 'forms/create_player.html', {'form': form})


@login_required
def add_goalkeeper_statistic(request, team, season):
    """Добавление статистики о голкипере"""
    form = AddGoalkeeperStatisticForm(team, season, request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('rating:team_players_in_season', team, season)
    form = AddGoalkeeperStatisticForm(team, season)
    context = {
        'form': form,
        'team': team,
        'season': season
    }
    return render(
        request,
        'forms/create_goalkeeper_statistic.html',
        context
    )


@login_required
def add_player_goalkeeper(request, team, season):
    """Добавление игрока в базу со страницы с добавлением статистики по
    вратарю. Использует туже форму что и полевой игрок, но из-за редиректа
    другая функция"""
    form = AddPlayerForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(
            'rating:create_goalkeeper_statistic', team, season)
    form = AddPlayerForm()
    return render(request, 'forms/create_player.html', {'form': form})


class SkaterStatisticUpdateView(UpdateView):
    form_class = EditStatisticForm
    pk_url_kwarg = 'id'
    template_name = "forms/create_statistic.html"

    def get_queryset(self):
        return Statistic.objects.filter(
            id=self.kwargs['id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team'] = self.kwargs['team']
        context['season'] = self.kwargs['season']
        return context

    def get_success_url(self, **kwargs):
        return reverse(
            'rating:team_players_in_season',
            kwargs={
                'team': self.kwargs['team'], 'season': self.kwargs['season']
            },
        )


class SkaterStatisticDeleteView(DeleteView):
    pk_url_kwarg = 'id'
    template_name = "forms/statistical_record_confirm_delete.html"

    def get_queryset(self):
        return Statistic.objects.filter(
            id=self.kwargs['id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team'] = self.kwargs['team']
        context['season'] = self.kwargs['season']
        return context

    def get_success_url(self, **kwargs):
        return reverse(
            'rating:team_players_in_season',
            kwargs={
                'team': self.kwargs['team'], 'season': self.kwargs['season']
            },
        )


@login_required
def edit_goalkeeper_statistic(request, team, season, id):
    """Редактирование статистики голкипера"""
    statistic = get_object_or_404(GoalkeeperStatistic, id=id)
    form = EditGoalkeeperStatisticForm(
        request.POST or None,
        instance=statistic
    )
    if form.is_valid():
        form.save()
        return redirect('rating:team_players_in_season', team, season)
    form = EditGoalkeeperStatisticForm(instance=statistic)
    context = {
        'form': form,
        'team': team,
        'season': season
    }
    return render(
        request,
        'forms/create_goalkeeper_statistic.html',
        context
    )


@login_required
def delete_goalkeeper_statistic(request, team, season, id):
    """удаление статистической записи по вратарю"""
    statistic = get_object_or_404(GoalkeeperStatistic, id=id)
    context = {
        'statistic': statistic,
        'team': team,
        'season': season
    }
    if request.method == 'GET':
        return render(
            request, 'forms/statistical_record_confirm_delete.html', context
        )
    elif request.method == 'POST':
        statistic.delete()
        messages.success(
            request, 'The statistical record has been deleted successfully.'
        )
        return redirect('rating:team_players_in_season', team, season)


def champions_leagues(request):
    champions = TeamForTable.objects.values(
        'rank', 'season__name', 'name__title', 'current_name').filter(
            rank='1').order_by('-season__name')
    champions2 = TeamForTable2Round.objects.values(
        'rank', 'season__name', 'name__title', 'current_name').filter(
            rank='1').order_by('-season__name')
    # most_goal_season = Statistic.objects.values(
    #     'season__name',
    # ).annotate(Max('goal')).order_by('-season__name')
    # for i in most_goal_season:
    #     print(i, type(i))
    champions_general_pre = sorted(
        chain(champions2, champions),
        key=lambda x: x['season__name'], reverse=True)
    champions_general = [champions_general_pre[0]]
    for i in champions_general_pre[1:]:
        if i['season__name'] != champions_general[-1]['season__name']:
            champions_general.append(i)
    context = {
        'champions_general': champions_general
    }
    template = 'posts/champions_leagues.html'
    return render(request, template, context)
