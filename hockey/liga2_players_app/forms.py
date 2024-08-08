from django import forms
from rating.models import Player, Season, Team

from .models import StatisticPlayer


class AddStatisticLiga2Form(forms.ModelForm):
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
        model = StatisticPlayer
        fields = (
            'name', 'team', 'season', 'position',
            'game', 'goal', 'assist', 'penalty'
        )
        widgets = {
        }

    # def __init__(self, team, season, *args):
    #     super(AddStatisticLiga2Form, self).__init__(*args)
    #     self.fields['team'].initial = Team.objects.get(
    #         title=team)
    #     self.fields['season'].initial = Season.objects.get(
    #         name=season)
    #     self.fields['name'].initial = Player.objects.last()

    # def __init__(self, team, *args):
    #     # print(args)
    #     self.team = Team.objects.get(
    #         title=team)
    #     super(AddStatisticLiga2Form, self).__init__(*args)


class EditStatisticLiga2Form(forms.ModelForm):
    class Meta:
        model = StatisticPlayer
        fields = (
            'name', 'position',
            'game', 'goal', 'assist', 'penalty'
        )
