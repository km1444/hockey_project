from django import forms

from .models import GoalkeeperStatistic, Player, Season, Statistic, Team


class AddStatisticForm(forms.ModelForm):
    team = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        label='Команда'
    )
    season = forms.ModelChoiceField(
        queryset=Season.objects.all(),
        label='Сезон'
    )
    name = forms.ModelChoiceField(
        queryset=Player.objects.all(),
        label='Игрок'
    )

    class Meta:
        model = Statistic
        fields = (
            'name', 'team', 'season', 'position',
            'game', 'goal', 'assist', 'penalty'
        )
        widgets = {
        }

    def __init__(self, team, season, *args):
        super(AddStatisticForm, self).__init__(*args)
        self.fields['team'].initial = Team.objects.get(
            title=team)
        self.fields['season'].initial = Season.objects.get(
            name=season)
        self.fields['name'].initial = Player.objects.last()


class EditStatisticForm(forms.ModelForm):
    class Meta:
        model = Statistic
        fields = (
            'name', 'position',
            'game', 'goal', 'assist', 'penalty'
        )


class AddPlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = (
            'name', 'year_of_birth',
        )


class AddGoalkeeperStatisticForm(forms.ModelForm):
    team = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        label='Команда'
    )
    season = forms.ModelChoiceField(
        queryset=Season.objects.all(),
        label='Сезон'
    )
    name = forms.ModelChoiceField(
        queryset=Player.objects.all(),
        label='Игрок'
    )

    class Meta:
        model = GoalkeeperStatistic
        fields = (
            'name', 'team', 'season', 'position',
            'game', 'goal_against', 'penalty'
        )

    def __init__(self, team, season, *args):
        super(AddGoalkeeperStatisticForm, self).__init__(*args)
        self.fields['team'].initial = Team.objects.get(
            title=team)
        self.fields['season'].initial = Season.objects.get(
            name=season)
        self.fields['name'].initial = Player.objects.last()


class EditGoalkeeperStatisticForm(forms.ModelForm):
    class Meta:
        model = GoalkeeperStatistic
        fields = (
            'name', 'team', 'season', 'position',
            'game', 'goal_against', 'penalty'
        )
