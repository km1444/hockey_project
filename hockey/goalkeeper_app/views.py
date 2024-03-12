from coach_app.models import CoachStatistic
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import render
from django.views.generic import ListView
from rating.models import GoalkeeperStatistic, Player


def goalkeeper_stat_alltime(request):
    goalkeeper_list = GoalkeeperStatistic.objects.values(
        'name__id', 'name__name').annotate(
            game=Sum('game')).order_by('-game').filter(game__gte=100)
    paginator = Paginator(goalkeeper_list, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    start_index = page_obj.start_index() - 1
    template = 'goalkeeper_app/goalkeeper_stat_alltime.html'
    context = {
        'page_obj': page_obj,
        'start_index': start_index,
        'table_name': 'Most Games Played (Goalie) Career 100+',
        'title': 'Вратари советского хоккея'
    }
    return render(request, template, context)


class GoalkeeperStatisticListView(ListView):
    model = GoalkeeperStatistic
    template_name = 'posts/profile_golie.html'
    context_object_name = 'page_obj'

    def get_queryset(self):
        return GoalkeeperStatistic.objects.filter(
            name__id=self.kwargs['pk']
        ).values(
            'name',
            'name__name',
            'age',
            'team__title',
            'season__name',
            'game',
            'goal_against',
            'penalty'
        ).order_by('season__name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = Player.objects.get(
            id=self.kwargs['pk'])
        context['position'] = 'Вратарь'
        context['count'] = context[
            'page_obj'].values('season').distinct().count()
        context['game'] = sum(elem['game'] for elem in context['page_obj'])
        context['goal_against'] = sum(
            elem['goal_against'] for elem in context['page_obj']
        )
        context['penalty'] = sum(
            elem['penalty'] for elem in context['page_obj']
        )
        context['amount_teams'] = context['page_obj'].values(
            'team__title').distinct().count()
        context['group_teams'] = context['page_obj'].values(
            'team__title').annotate(
                game=Sum('game'),
                goal_against=Sum('goal_against'),
                penalty=Sum('penalty')).order_by('-game')
        context['goalkeeper'] = True
        context['coach_obj'] = CoachStatistic.objects.filter(
            name__id=self.kwargs['pk']).values(
                'name',
                'name__name',
                'age',
                'team__title',
                'season__name',
                'final_position',
                'full_season',
                'fired_season',
                'came_season').order_by('season__name')
        if context['coach_obj']:
            context['coach'] = True
        return context
