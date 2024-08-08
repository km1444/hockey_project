# from django.contrib.auth.decorators import login_required
# from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from liga2_players_app.utils import ContextFormMixin
from rating.forms import AddPlayerForm
from rating.models import Player, Season, Team

from .forms import AddGoalkeeperStatisticLiga2Form, EditGoalkeeperStatLiga2Form
from .models import GoalkeeperStatisticLiga2


class AddKeeperStatLiga2(ContextFormMixin, CreateView):
    form_class = AddGoalkeeperStatisticLiga2Form
    template_name = "forms/liga2/liga2_create_goalkeeper_statistic.html"

    def get_initial(self):
        initial = super(AddKeeperStatLiga2, self).get_initial()
        initial['team'] = Team.objects.get(title=self.kwargs['team'])
        initial['season'] = Season.objects.get(name=self.kwargs['season'])
        initial['name'] = Player.objects.last()
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['discription'] = 'Добавление статистики вратаря первой лиги'
        context['discription_button'] = 'Сохранить запись'
        return self.get_mixin_context(context)

    def get_success_url(self, **kwargs):
        return reverse(
            'liga2_players:players_team_season',
            kwargs={
                'team': self.kwargs['team'], 'season': self.kwargs['season']
            },
        )


class AddPlayerGoalkeeper(ContextFormMixin, CreateView):
    form_class = AddPlayerForm
    template_name = "forms/create_player.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)

    def get_success_url(self, **kwargs):
        return reverse(
            'goalkeeper_liga2:add_goalkeeper_statistic_liga2',
            kwargs={
                'team': self.kwargs['team'], 'season': self.kwargs['season']
            },
        )


class EditGoalkeeperStatLiga2(ContextFormMixin, UpdateView):
    form_class = EditGoalkeeperStatLiga2Form
    pk_url_kwarg = 'id'
    template_name = "forms/liga2/liga2_create_goalkeeper_statistic.html"

    def get_queryset(self):
        return GoalkeeperStatisticLiga2.objects.filter(
            id=self.kwargs['id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['discription'] = (
            'Редактирование статистики вратаря первой лиги')
        context['discription_button'] = 'Сохранить изменения'
        return self.get_mixin_context(context)

    def get_success_url(self, **kwargs):
        return reverse(
            'liga2_players:players_team_season',
            kwargs={
                'team': self.kwargs['team'], 'season': self.kwargs['season']
            },
        )


class DeleteGoalkeeperStatLiga2(ContextFormMixin, DeleteView):
    pk_url_kwarg = 'id'
    template_name = "forms/liga2/liga2_statistical_record_confirm_delete.html"
    context_object_name = 'statistic'

    def get_queryset(self):
        return GoalkeeperStatisticLiga2.objects.filter(id=self.kwargs['id'])

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


class ListGoalkeepersLiga2(ListView):
    model = GoalkeeperStatisticLiga2
    template_name = (
        'liga2_players/most_games_played_in_liga2_goalie_career.html')
    context_object_name = 'goalkeeper_list'
    paginate_by = 25

    def get_queryset(self):
        return GoalkeeperStatisticLiga2.objects.values(
            'name__id', 'name__name').annotate(
                game=Sum('game')).order_by('-game')[:100]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_obj = context['paginator'].get_page(self.request.GET.get('page'))
        context['start_index'] = page_obj.start_index() - 1
        context['title'] = 'Лучшие вратари советского хоккея в первой лиге'
        context['table_name'] = (
            'Most Games Played in First League(Goalie) Career 100+')
        return context
