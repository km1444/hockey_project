from django.db.models import Sum

from .models import StatisticPlayer


class SeasonStatisticMixin:
    def get_mixin_queryset(self, *args, **kwargs):
        return StatisticPlayer.objects.filter(
            season__name=self.kwargs['season']).values(
                'name__id', 'name__name', 'age', 'team__slug').annotate(
                    game=Sum('game'),
                    goal=Sum('goal'),
                    assist=Sum('assist'),
                    point=Sum('point'),
                    penalty=Sum('penalty'))


class PrevNextSeasonMixin:
    def get_mixin_context(self, context, **kwargs):
        context['previous_season'] = '-'.join(
            list(
                map(
                    lambda x: str(int(x) - 1),
                    self.kwargs['season'].split('-')
                )))
        context['next_season'] = '-'.join(
            list(
                map(
                    lambda x: str(int(x) + 1),
                    self.kwargs['season'].split('-')
                )))
        context['season'] = self.kwargs['season']
        context.update(kwargs)
        return context


class ContextFormMixin:
    def get_mixin_context(self, context, **kwargs):
        context['team'] = self.kwargs['team']
        context['season'] = self.kwargs['season']
        context.update(kwargs)
        return context
