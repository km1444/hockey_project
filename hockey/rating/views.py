# from aggregates import StringAgg
# from django.core.paginator import Paginator
# from django.db import models
from django.db.models import Q, Sum
# from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from .models import (
    DescriptionTable, GolkeeperStatistic, Player, Playoff, Statistic, Team,
    TeamForTable, TeamForTable2, TeamForTable2Round, TeamForTable2Round2,
    TeamForTable2Round3, TeamForTable3, TeamForTable4,
)
from .secondary import (
    prev_next_season, top_goal, top_point, top_season_goal, top_season_point,
)


def index(request):
    total_points_for_players = Statistic.objects.values(
        'name__id', 'name__name').annotate(
            game=Sum('game'),
            point=Sum('point')).order_by(
                '-point', 'game')[:20]
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
    goalkeepers = GolkeeperStatistic.objects.filter(
        team__title=team, season__name=season
    ).order_by('-game')
    team_info = TeamForTable.objects.filter(
        name__title=team,
        season__name=season
    )
    template = 'posts/team_players_in_season.html'
    context = {
        'team': team,
        'team_info': team_info,
        'season': season,
        'previous_season': prev_next_season(season)[1],
        'next_season': prev_next_season(season)[0],
        'page_obj': team_statistic,
        'goalkeepers': goalkeepers,
    }
    return render(request, template, context)


def player_detail(request, id):
    player = get_object_or_404(Player, id=id)
    player_seasons = player.statistics.order_by('season__name')
    if player_seasons:
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
        count = player_seasons.values('season').distinct().count()
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
    else:
        player_seasons = player.golkeeperstatistic.order_by('season__name')
        game = sum(i.game for i in player_seasons)
        goal_against = sum(i.goal_against for i in player_seasons)
        penalty = sum(i.penalty for i in player_seasons)
        amount_teams = player_seasons.values('team__title').distinct().count()
        group_teams = player_seasons.values('team__title').annotate(
            game=Sum('game'),
            goal_against=Sum('goal_against'),
            penalty=Sum('penalty')
        ).order_by('-game')
        count = player_seasons.values('season').distinct().count()
        position = player_seasons[0].position
        template = 'posts/profile_golie.html'
        context = {
            'name': player,
            'count': count,
            'page_obj': player_seasons,
            'game': game,
            'goal_against': goal_against,
            'penalty': penalty,
            'position': position,
            'group_teams': group_teams,
            'amount_teams': amount_teams,
        }
    return render(request, template, context)


class GolkeeperStatisticListView(ListView):
    model = GolkeeperStatistic
    template_name = 'posts/profile_golie.html'
    context_object_name = 'page_obj'

    def get_queryset(self):
        return GolkeeperStatistic.objects.filter(
            name__id=self.kwargs['pk']).order_by('-season')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = Player.objects.get(
            id=self.kwargs['pk'])
        context['position'] = context['page_obj'][0].position
        context['count'] = context[
            'page_obj'].values('season').distinct().count()
        context['game'] = sum(elem.game for elem in context['page_obj'])
        return context


def best_of_season(request, season, stat_rule):
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
        'stat_rule': stat_rule
    }
    return render(request, template, context)


def all_time_all_player_one_team(request, team):
    team = Team.objects.get(title=team)
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


def statistic(request, stat_rule):
    rule = stat_rule.split('_')
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
        )[:20]
        context = {
            'page_obj': total_for_players,
            'table_name': 'Career Leaders for' + ' ' + f'{rule[0].title()}''s'
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
        )[:20]
        context = {
            'page_obj': total_for_players,
            'table_name':
            'Single Season Leaders for' + ' ' + f'{rule[0].title()}''s'
        }
    template = 'posts/index.html'
    return render(request, template, context)


def create_table(request, season):
    teams = TeamForTable.objects.filter(season__name=season).order_by('rank')
    teams2 = TeamForTable2.objects.filter(season__name=season).order_by('rank')
    teams3 = TeamForTable3.objects.filter(season__name=season).order_by('rank')
    teams4 = TeamForTable4.objects.filter(season__name=season).order_by('rank')
    teams2round = TeamForTable2Round.objects.filter(
        season__name=season).order_by('rank')
    teams2round2 = TeamForTable2Round2.objects.filter(
        season__name=season).order_by('rank')
    teams2round3 = TeamForTable2Round3.objects.filter(
        season__name=season).order_by('rank')
    playoff = Playoff.objects.filter(season__name=season).order_by('number')
    try:
        description_table = DescriptionTable.objects.get(season__name=season)
    except DescriptionTable.DoesNotExist:
        description_table = ''
    # print(description_table.__dict__)
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
    team = Team.objects.get(title=team)
    query_list = Statistic.objects.filter(
        team__title=team).values(
            'name__id',
            'name__name').annotate(
                game=Sum('game'),
                goal=Sum('goal'),
                assist=Sum('assist'),
                penalty=Sum('penalty'))
    top_10_game = query_list.order_by('-game')[:10]
    top_10_goal = query_list.order_by('-goal')[:10]
    top_10_assist = query_list.order_by('-assist')[:10]
    top_10_penalty = query_list.order_by('-penalty')[:10]
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
    team = Team.objects.get(title=team)
    top_10_goal = Statistic.objects.filter(
        team__title=team).values(
            'name__id',
            'name__name',
            'goal',
            'season__name').order_by(
                '-goal')[:10]
    top_10_assist = Statistic.objects.filter(
        team__title=team).values(
            'name__id',
            'name__name',
            'assist',
            'season__name').order_by(
                '-assist')[:10]
    top_10_point = Statistic.objects.filter(
        team__title=team).values(
            'name__id',
            'name__name',
            'point',
            'season__name').order_by(
                '-point')[:10]
    top_10_penalty = Statistic.objects.filter(
        team__title=team).values(
            'name__id',
            'name__name',
            'penalty',
            'season__name').order_by(
                '-penalty')[:10]
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
    """ функция формирования содержимого страницы с историей команды """
    team_view = TeamForTable.objects.filter(
        name__title=team).order_by('-season__name')
    team = Team.objects.get(title=team)
    count_season = team_view.count()
    context = {
        'team_view': team_view,
        # 'team_view_2round': team_view_2round,
        'team': team,
        'count_season': count_season,
        'top_goal': top_goal(team),
        'top_point': top_point(team),
        'top_s_goal': top_season_goal(team),
        'top_s_point': top_season_point(team)
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
