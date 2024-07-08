from django.contrib import admin

from .models import StatisticPlayer


@admin.register(StatisticPlayer)
class StatisticPlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'season', 'team', 'point')
    search_fields = ('name__name',)
    list_filter = ('name',)
    fields = [
        'name', 'team', 'season', 'position',
        ('game', 'goal', 'assist', 'penalty')
    ]
    empty_value_display = '-empty-'
