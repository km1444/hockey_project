from django import forms
from rating.models import Season, Team

from .models import (
    AdditionalTournament, AdditionalTournamentSecond,
    AdditionalTournamentWithoutPoints, TeamInTable1gr, TransitionTournament,
    TransitionWithoutPoints,
)


class AddTeamForm(forms.ModelForm):
    team_name = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        label='Команда'
    )
    season = forms.ModelChoiceField(
        queryset=Season.objects.all(),
        label='Сезон'
    )
    transition_tournament = forms.ModelChoiceField(
        queryset=TransitionTournament.objects.all(),
        label='Переходный турнир',
        required=False
    )
    transition_tournament_without_points = forms.ModelChoiceField(
        queryset=TransitionWithoutPoints.objects.all(),
        label='Переходный турнир без учета ранее набранных очков',
        required=False
    )
    additional_tournament = forms.ModelChoiceField(
        queryset=AdditionalTournament.objects.all(),
        label='Дополнительный турнир',
        required=False
    )
    additional_tournament_second = forms.ModelChoiceField(
        queryset=AdditionalTournamentSecond.objects.all(),
        label='Второй дополнительный турнир',
        required=False
    )
    additional_tournament_without_points = forms.ModelChoiceField(
        queryset=AdditionalTournamentWithoutPoints.objects.all(),
        label='Дополнительный турнир без учета ранее набранных очков',
        required=False
    )

    class Meta:
        model = TeamInTable1gr
        fields = (
            'rank', 'team_name', 'current_name',
            'season', 'games',
            'wins', 'ties', 'losses', 'points',
            'transition_tournament',
            'transition_serie',
            'additional_tournament',
            'additional_tournament_second',
            'transition_tournament_without_points',
            'additional_tournament_without_points'
        )
        widgets = {
        }

    def __init__(self, season, *args):
        super(AddTeamForm, self).__init__(*args)
        self.fields['season'].initial = Season.objects.get(
            name=season)
        self.fields[
            'transition_tournament'
        ].queryset = TransitionTournament.objects.filter(season__name=season)
        self.fields[
            'additional_tournament'
        ].queryset = AdditionalTournament.objects.filter(season__name=season)
        self.fields[
            'additional_tournament_second'
        ].queryset = AdditionalTournamentSecond.objects.filter(
            season__name=season)
        self.fields[
            'transition_tournament_without_points'
        ].queryset = TransitionWithoutPoints.objects.filter(
            season__name=season)
        self.fields[
            'additional_tournament_without_points'
        ].queryset = AdditionalTournamentWithoutPoints.objects.filter(
            season__name=season)


class AddTeamTransitionTournamentForm(forms.ModelForm):
    team_name = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        label='Команда'
    )
    season = forms.ModelChoiceField(
        queryset=Season.objects.all(),
        label='Сезон'
    )

    class Meta:
        model = TransitionTournament
        fields = (
            'rank_real', 'rank_pict', 'team_name', 'current_name',
            'season', 'games',
            'wins', 'ties', 'losses', 'points',
        )
        widgets = {
        }

    def __init__(self, season, *args):
        super(AddTeamTransitionTournamentForm, self).__init__(*args)
        self.fields['season'].initial = Season.objects.get(
            name=season)


class AddTeamAdditionalTournamentForm(forms.ModelForm):
    team_name = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        label='Команда'
    )
    season = forms.ModelChoiceField(
        queryset=Season.objects.all(),
        label='Сезон'
    )

    class Meta:
        model = AdditionalTournament
        fields = (
            'rank', 'team_name', 'current_name',
            'season', 'games',
            'wins', 'ties', 'losses', 'points',
        )
        widgets = {
        }

    def __init__(self, season, *args):
        super(AddTeamAdditionalTournamentForm, self).__init__(*args)
        self.fields['season'].initial = Season.objects.get(
            name=season)
        self.fields['team_name'].initial = Team.objects.last()


class CreateTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = (
            'title', 'city', 'slug'
        )


class EditTeamInTransitionTournamentForm(forms.ModelForm):
    class Meta:
        model = TransitionTournament
        fields = (
            'rank_real', 'rank_pict', 'team_name', 'current_name',
            'season', 'games',
            'wins', 'ties', 'losses', 'points',
        )


class EditTeamInBasicTournamentForm(forms.ModelForm):
    class Meta:
        model = TeamInTable1gr
        fields = (
            'rank', 'team_name', 'current_name',
            'season', 'games',
            'wins', 'ties', 'losses', 'points',
            'transition_tournament',
            'transition_serie',
            'additional_tournament'
        )


class EditTeamInAdditionalTournamentForm(forms.ModelForm):
    class Meta:
        model = AdditionalTournament
        fields = (
            'rank', 'team_name', 'current_name',
            'season', 'games',
            'wins', 'ties', 'losses', 'points',
        )
