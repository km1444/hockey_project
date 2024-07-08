from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import redirect, render
from rating.forms import AddPlayerForm

from .forms import AddGoalkeeperStatisticLiga2Form
from .models import GoalkeeperStatisticLiga2


@login_required
def add_goalkeeper_statistic_liga2(request, team, season):
    """Добавление статистики о голкипере первой лиги"""
    form = AddGoalkeeperStatisticLiga2Form(team, season, request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('liga2_players:players_team_season', team, season)
    form = AddGoalkeeperStatisticLiga2Form(team, season)
    context = {
        'form': form,
        'team': team,
        'season': season
    }
    return render(
        request,
        'forms/liga2/liga2_create_goalkeeper_statistic.html',
        context
    )


@login_required
def add_player_goalkeeper(request, team, season):
    """Добавление игрока в базу со страницы с добавлением статистики по
    вратарю первой лиги. Использует туже форму что и полевой игрок,
    но из-за редиректа другая функция"""
    form = AddPlayerForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(
            'goalkeeper_liga2:add_goalkeeper_statistic_liga2', team, season)
    form = AddPlayerForm()
    return render(request, 'forms/create_player.html', {'form': form})


def goalkeepers_in_the_first_league(request):
    goalkeeper_list = GoalkeeperStatisticLiga2.objects.values(
        'name__id', 'name__name').annotate(
            game=Sum('game')).order_by('-game').filter(game__gte=10)
    paginator = Paginator(goalkeeper_list, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    start_index = page_obj.start_index() - 1
    template = 'liga2_players/most_games_played_in_liga2_goalie_career.html'
    context = {
        'page_obj': page_obj,
        'start_index': start_index,
        'table_name': 'Most Games Played in First League(Goalie) Career 100+',
        'title': 'Вратари советского хоккея в первой лиге'
    }
    return render(request, template, context)
