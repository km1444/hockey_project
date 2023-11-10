from django.db.models import Sum
from django.shortcuts import render
from miscellaneous.forms import FilterForm
from rating.models import Statistic


def filter_start(request):
    form = FilterForm(request.POST or None)
    if form.is_valid():
        return filter_view(
            request,
            season_start=form.cleaned_data['name'],
            season_end=form.cleaned_data['name2'],
            types_stat=form.cleaned_data['types']
        )
    form = FilterForm()
    context = {
        'form': form,
    }
    return render(request, 'miscellaneous/filter.html', context)


def filter_view(request, season_start, season_end, types_stat):
    total_points_for_players = Statistic.objects.filter(
        season__name__range=[season_start, season_end]).values(
            'name__id', 'name__name').annotate(
                game=Sum('game'),
                goal=Sum('goal'),
                assist=Sum('assist'),
                point=Sum('point'),
                penalty=Sum('penalty')).order_by(
                    f'-{types_stat}', 'game', '-point', '-goal')[:50]
    template = 'miscellaneous/filter.html'
    form = FilterForm()
    form.fields['name'].initial = season_start
    form.fields['name2'].initial = season_end
    form.fields['types'].initial = types_stat
    table_name = f"{season_start} - {season_end} ({types_stat})"
    context = {
        'form': form,
        'page_obj': total_points_for_players,
        'table_name': table_name,
        'types_stat': types_stat,
    }
    return render(request, template, context)
