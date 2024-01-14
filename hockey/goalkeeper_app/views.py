from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import render
from rating.models import GoalkeeperStatistic


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
