from django import forms
from rating.models import Season


class FilterForm(forms.ModelForm):
    stat_types = (
        ('goal', 'goal'),
        ('game', 'game'),
        ('assist', 'assist'),
        ('point', 'point'),
    )
    name = forms.ModelChoiceField(
        queryset=Season.objects.all().order_by('name'),
        label='Начало'
    )
    name2 = forms.ModelChoiceField(
        queryset=Season.objects.all().order_by('name'),
        label='Конец'
    )
    types = forms.ChoiceField(
        choices=stat_types, label='Вариант')

    class Meta:
        model = Season
        fields = (
            'name',
        )

    # def clean_name2(self):
    #     data_2 = self.cleaned_data['name2']
    #     data = self.cleaned_data['name']
    #     if data.name > data_2.name:
    #         raise forms.ValidationError(
    #             'Вторая дата должна быть позже или равна первой')
    #     return data_2
