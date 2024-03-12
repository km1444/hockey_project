from django import forms

from .models import CoachStatistic, Player, Season, Team


class AddCoachForm(forms.ModelForm):
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
        label='Тренер'
    )

    class Meta:
        model = CoachStatistic
        fields = (
            'name', 'team', 'season', 'final_position',
            'full_season', 'fired_season', 'came_season'
        )
        widgets = {
        }

    def __init__(self, team, season, *args):
        super(AddCoachForm, self).__init__(*args)
        self.fields['team'].initial = Team.objects.get(
            title=team)
        self.fields['season'].initial = Season.objects.get(
            name=season)
        self.fields['name'].initial = Player.objects.last()
