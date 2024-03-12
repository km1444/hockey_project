from django.shortcuts import redirect, render

from .forms import AddCoachForm


def create_coach_record(request, team, season):
    """Функция добавления статистической записи об игроке,
    с автозаполнением полей с названием команды и сезона"""
    form = AddCoachForm(team, season, request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('rating:team_players_in_season', team, season)
    form = AddCoachForm(team, season)
    context = {
        'form': form,
        'team': team,
        'season': season
    }
    return render(request, 'forms/create_coach_record.html', context)
