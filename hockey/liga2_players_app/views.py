import operator

from functools import reduce

# from django.contrib.auth.decorators import login_required
# from django.core.paginator import Paginator
from django.db.models import Max, Q, Sum, Avg, Count
from django.shortcuts import get_object_or_404, reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from goalkeeper_liga2_app.models import GoalkeeperStatisticLiga2
from liga2_seasons_app.models import TeamInTable1gr, TeamInTable2gr
from rating.forms import AddPlayerForm
from rating.models import Player, Season, Team, TeamForTable

from .forms import AddStatisticLiga2Form, EditStatisticLiga2Form
from .models import StatisticPlayer
from .utils import ContextFormMixin, PrevNextSeasonMixin, SeasonStatisticMixin

# from rating.secondary import prev_next_season


class PlayerStatisticsByCategory(ListView):
    model = StatisticPlayer
    template_name = 'liga2_seasons/liga2_index.html'
    context_object_name = 'list_of_scorers'
    paginate_by = 25

    # pl_list = StatisticPlayer.objects.filter(
    #     season__name__range=('1970-71', '1979-80'), age='43').values(
    #         'age').annotate(
    #             players_count=Count('name'),
    #             game_all=Sum('game'),
    #             games_avg=Avg('game'))
    # summury_list = pl_list.aggregate(avg_game=Avg('games_avg'))
    # for pl in pl_list:
    #     print(pl)
    # print(summury_list)

    def get_queryset(self):
        rule = self.kwargs['stat_rule'].split('_')
        if rule[1] == 'career':
            return StatisticPlayer.objects.values(
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
        elif rule[1] == 'season':
            return StatisticPlayer.objects.values(
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
        elif rule[1] == 'yearly':
            best_goals = StatisticPlayer.objects.values(
                'season__name'
            ).annotate(
                goal=Max('goal'))
            q_object = reduce(operator.or_, (Q(**x) for x in best_goals))
            return StatisticPlayer.objects.values(
                'name__id',
                'name__name',
                'season__name',
                'goal',
                'game'
            ).filter(q_object).order_by('season__name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dict_rule = {
            'goal': 'голам',
            'assist': 'передачам',
            'point': 'очкам',
            'penalty': 'штрафным минутам',
            'game': 'матчам'
        }
        rule = self.kwargs['stat_rule'].split('_')
        page_obj = context['paginator'].get_page(self.request.GET.get('page'))
        context['start_index'] = page_obj.start_index() - 1
        if rule[1] == 'career':
            context['table_name'] = (
                'Most ' + f'{rule[0].title()}''s' + ' Career League 1')
            context['table_description'] = (
                'Лидеры по ' + f'{dict_rule[rule[0]]}'
                + ' за карьеру в первой лиге')
        elif rule[1] == 'season':
            context['table_name'] = (
                'Most ' + f'{rule[0].title()}''s' + ' Single Season League 1')
            context['table_description'] = (
                'Лидеры по ' + f'{dict_rule[rule[0]]}'
                + ' за сезон в первой лиге')
        elif rule[1] == 'yearly':
            context['table_name'] = (
                'Yearly Leaders for ' + f'{rule[0].title()}''s League 1')
            context['table_description'] = (
                'Лучшие голеадоры по сезонам'
            )
        context['title'] = 'Лучшие бомбардиры советского хоккея в первой лиге'
        return context


class PlayersTeamSeason(PrevNextSeasonMixin, ListView):
    template_name = 'liga2_players/liga2_players_team_season.html'
    context_object_name = 'page_obj'
    # model = StatisticPlayer

    def get_queryset(self, *args, **kwargs):
        return StatisticPlayer.objects.filter(
            team__title=self.kwargs['team'],
            season__name=self.kwargs['season']).values(
                'id',
                'name',
                'name__name',
                'age',
                'game',
                'goal',
                'assist',
                'point',
                'penalty').order_by('-point', '-goal', 'game')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team'] = get_object_or_404(Team, title=self.kwargs['team'])
        context['season'] = get_object_or_404(
            Season, name=self.kwargs['season'])
        context['info_of_team'] = TeamInTable1gr.objects.filter(
            team_name__title=self.kwargs['team'],
            season__name=self.kwargs['season'])
        context['info_of_team_2gr'] = TeamInTable2gr.objects.filter(
            team_name__title=self.kwargs['team'],
            season__name=self.kwargs['season'])
        context['info_of_team_from_major'] = TeamForTable.objects.filter(
            name__title=self.kwargs['team'],
            season__name=self.kwargs['season'])
        context['goalkeepers'] = GoalkeeperStatisticLiga2.objects.filter(
            team__title=self.kwargs['team'],
            season__name=self.kwargs['season']).values(
                'id',
                'name',
                'name__name',
                'age',
                'game',
                'goal_against',
                'penalty').order_by('-game')
        return self.get_mixin_context(context)


class LeadersGoalsSeason(PrevNextSeasonMixin, SeasonStatisticMixin, ListView):
    """Лидеры по голам в сезоне. Статистика игроков в сезоне - голы"""
    model = StatisticPlayer
    template_name = (
        'liga2_players/liga2_statistical_leaders_of_the_season.html')
    context_object_name = 'players_list'

    def get_queryset(self, *args, **kwargs):
        return self.get_mixin_queryset(self, *args, **kwargs).order_by(
            '-goal', 'game')[:25]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_table'] = 'Goals leaders'
        context['column_heading'] = 'G'
        context['link'] = 'liga2_players:leaders_goals_season'
        return self.get_mixin_context(context)


class LeadersAssistsSeason(
        PrevNextSeasonMixin, SeasonStatisticMixin, ListView):
    """Лидеры по передачам в сезоне. Статистика игроков в сезоне - передачи"""
    model = StatisticPlayer
    template_name = (
        'liga2_players/liga2_statistical_leaders_of_the_season.html')
    context_object_name = 'players_list'

    def get_queryset(self, *args, **kwargs):
        return self.get_mixin_queryset(self, *args, **kwargs).order_by(
            '-assist', 'game')[:22]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_table'] = 'Assists leaders'
        context['column_heading'] = 'A'
        context['link'] = 'liga2_players:leaders_assists_season'
        return self.get_mixin_context(context)


class LeadersPointsSeason(PrevNextSeasonMixin, SeasonStatisticMixin, ListView):
    """Лидеры по очкам в сезоне. Статистика игроков в сезоне - очки"""
    model = StatisticPlayer
    template_name = (
        'liga2_players/liga2_statistical_leaders_of_the_season.html')
    context_object_name = 'players_list'

    def get_queryset(self, *args, **kwargs):
        return self.get_mixin_queryset(self, *args, **kwargs).order_by(
            '-point', '-goal', 'game')[:23]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_table'] = 'Points leaders'
        context['column_heading'] = 'PTS'
        context['link'] = 'liga2_players:leaders_points_season'
        return self.get_mixin_context(context)


class LeadersPenaltysSeason(
        PrevNextSeasonMixin, SeasonStatisticMixin, ListView):
    """Лидеры по очкам в сезоне. Статистика игроков в сезоне - очки"""
    model = StatisticPlayer
    template_name = (
        'liga2_players/liga2_statistical_leaders_of_the_season.html')
    context_object_name = 'players_list'

    def get_queryset(self, *args, **kwargs):
        return self.get_mixin_queryset(self, *args, **kwargs).order_by(
            '-penalty', 'game')[:24]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_table'] = 'Penalty leaders'
        context['column_heading'] = 'PIM'
        context['link'] = 'liga2_players:leaders_penaltys_season'
        return self.get_mixin_context(context)


class AddStatisticLiga2(ContextFormMixin, CreateView):
    form_class = AddStatisticLiga2Form
    template_name = "forms/liga2/liga2_create_statistic.html"

    def get_initial(self):
        initial = super(AddStatisticLiga2, self).get_initial()
        initial['team'] = Team.objects.get(title=self.kwargs['team'])
        initial['season'] = Season.objects.get(name=self.kwargs['season'])
        initial['name'] = Player.objects.last()
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)

    def get_success_url(self, **kwargs):
        return reverse(
            'liga2_players:players_team_season',
            kwargs={
                'team': self.kwargs['team'], 'season': self.kwargs['season']
            },
        )


class AddPlayerLiga2(ContextFormMixin, CreateView):
    form_class = AddPlayerForm
    template_name = "forms/create_player.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)

    def get_success_url(self, **kwargs):
        return reverse(
            'liga2_players:create_statistic_liga2',
            kwargs={
                'team': self.kwargs['team'], 'season': self.kwargs['season']
            },
        )


class SkaterStatisticLiga2UpdateView(ContextFormMixin, UpdateView):
    form_class = EditStatisticLiga2Form
    pk_url_kwarg = 'id'
    template_name = "forms/liga2/liga2_create_statistic.html"

    def get_queryset(self):
        return StatisticPlayer.objects.filter(
            id=self.kwargs['id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)

    def get_success_url(self, **kwargs):
        return reverse(
            'liga2_players:players_team_season',
            kwargs={
                'team': self.kwargs['team'], 'season': self.kwargs['season']
            },
        )


class DeleteSkaterStatLiga2DeleteView(ContextFormMixin, DeleteView):
    pk_url_kwarg = 'id'
    template_name = "forms/liga2/liga2_statistical_record_confirm_delete.html"
    context_object_name = 'statistic'

    def get_queryset(self):
        return StatisticPlayer.objects.filter(id=self.kwargs['id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)

    def get_success_url(self, **kwargs):
        return reverse(
            'liga2_players:players_team_season',
            kwargs={
                'team': self.kwargs['team'], 'season': self.kwargs['season']
            },
        )
