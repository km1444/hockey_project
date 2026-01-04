from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from rating.secondary import prev_next_season

from .forms import (
    AddTeamAdditionalTournamentForm, AddTeamForm,
    AddTeamTransitionTournamentForm, CreateTeamForm,
    EditTeamInAdditionalTournamentForm, EditTeamInBasicTournamentForm,
    EditTeamInTransitionTournamentForm,
)
from .models import (
    AdditionalTournament, AdditionalTournamentSecond,
    AdditionalTournamentWithoutPoints, AdditionalTournamentWithoutPointsSecond,
    DescriptionTable, TeamInTable1gr, TeamInTable2gr, TransitionTournament,
    TransitionWithoutPoints,
)


def liga2_index(request):
    template = 'liga2_seasons/liga2_index.html'
    context = {
    }
    return render(request, template, context)


def liga2_season(request, season):
    template = 'liga2_seasons/liga2_season.html'
    teams_transition = TransitionTournament.objects.filter(
        season__name=season).select_related('team_name').order_by('rank_real')
    teams_transition_without_points = TransitionWithoutPoints.objects.filter(
        season__name=season).select_related('team_name').order_by('rank')
    teams = TeamInTable1gr.objects.filter(
        season__name=season).select_related('team_name').order_by('rank')
    teams_east = TeamInTable2gr.objects.filter(
        season__name=season).select_related('team_name').order_by('rank')
    additional_tournament = AdditionalTournament.objects.filter(
        season__name=season).select_related('team_name').order_by('rank')
    additional_tournament_second = AdditionalTournamentSecond.objects.filter(
        season__name=season).select_related('team_name').order_by('rank')
    additional_tournament_without_points = (
        AdditionalTournamentWithoutPoints.objects.filter(
            season__name=season).select_related('team_name').order_by('rank'))
    additional_tournament_without_points_second = (
        AdditionalTournamentWithoutPointsSecond.objects.filter(
            season__name=season).select_related('team_name').order_by('rank'))
    details_season = False
    try:
        description_table = DescriptionTable.objects.get(season__name=season)
        if len(description_table.description_season.split()) > 40:
            details_season = True
    except DescriptionTable.DoesNotExist:
        description_table = ''
    context = {
        'previous_season': prev_next_season(season)[1],
        'next_season': prev_next_season(season)[0],
        'season': season,
        'teams_transition': teams_transition,
        'teams_transition_without_points': teams_transition_without_points,
        'teams': teams,
        'teams_east': teams_east,
        'additional_tournament': additional_tournament,
        'additional_tournament_second': additional_tournament_second,
        'additional_tournament_without_points':
        additional_tournament_without_points,
        'additional_tournament_without_points_second':
        additional_tournament_without_points_second,
        'description_table': description_table,
        'details_season': details_season,
    }
    return render(request, template, context)


@login_required
def add_team(request, season):
    form = AddTeamForm(season, request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('liga2_seasons:liga2_season', season)
    form = AddTeamForm(season)
    # additional_tournament = AdditionalTournament.objects.filter(
    #     season__name=season)
    context = {
        'form': form,
        'season': season,
        # 'additional_tournament': additional_tournament,
    }
    return render(request, 'forms/liga2/add_team.html', context)


@login_required
def add_team_trans_tournament(request, season):
    form = AddTeamTransitionTournamentForm(season, request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('liga2_seasons:liga2_season', season)
    form = AddTeamTransitionTournamentForm(season)
    context = {
        'form': form,
        'season': season
    }
    return render(
        request, 'forms/liga2/add_team_trans_tournament.html', context)


@login_required
def add_team_addit_tournament(request, season):
    form = AddTeamAdditionalTournamentForm(season, request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('liga2_seasons:liga2_season', season)
    form = AddTeamAdditionalTournamentForm(season)
    context = {
        'form': form,
        'season': season
    }
    return render(
        request, 'forms/liga2/add_team_addit_tournament.html', context)


@login_required
def create_team(request, season):
    """Добавление команды в базу"""
    # def get_http(request):
    #     url = request.META.get('HTTP_REFERER')
    #     return url
    form = CreateTeamForm(request.POST or None)
    # home = get_http(request)
    if form.is_valid():
        form.save()
        return redirect('liga2_seasons:liga2_season', season)
    # form = CreateTeamForm()
    # home = get_http()
    # print(home)
    return render(request, 'forms/liga2/create_team.html', {'form': form})


@login_required
def edit_team_in_transition_tournament(request, season, pk):
    team = get_object_or_404(TransitionTournament, id=pk)
    form = EditTeamInTransitionTournamentForm(
        request.POST or None,
        instance=team
    )
    if form.is_valid():
        form.save()
        return redirect('liga2_seasons:liga2_season', season)
    form = EditTeamInTransitionTournamentForm(instance=team)
    context = {
        'form': form,
        'season': season
    }
    return render(
        request,
        'forms/liga2/add_team_trans_tournament.html',
        context
    )


@login_required
def edit_team_in_basic_tournament(request, season, pk):
    team = get_object_or_404(TeamInTable1gr, id=pk)
    form = EditTeamInBasicTournamentForm(request.POST or None, instance=team)
    if form.is_valid():
        form.save()
        return redirect('liga2_seasons:liga2_season', season)
    form = EditTeamInBasicTournamentForm(instance=team)
    context = {
        'form': form,
        'season': season
    }
    return render(request, 'forms/liga2/add_team.html', context)


@login_required
def edit_team_in_additional_tournament(request, season, pk):
    team = get_object_or_404(AdditionalTournament, id=pk)
    form = EditTeamInAdditionalTournamentForm(
        request.POST or None,
        instance=team
    )
    if form.is_valid():
        form.save()
        return redirect('liga2_seasons:liga2_season', season)
    form = EditTeamInAdditionalTournamentForm(instance=team)
    context = {
        'form': form,
        'season': season
    }
    return render(
        request,
        'forms/liga2/add_team_addit_tournament.html',
        context
    )
