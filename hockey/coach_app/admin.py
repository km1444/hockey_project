from django.contrib import admin

from .models import CoachStatistic


class CoachStatisticAdmin(admin.ModelAdmin):
    list_display = ('name', 'season', 'team')
    search_fields = ('name__name',)
    list_filter = ('name',)
    fields = [
        'name', 'team', 'season', 'final_position',
        'full_season', 'fired_season', 'came_season'
    ]
    empty_value_display = '-empty-'


admin.site.register(CoachStatistic, CoachStatisticAdmin)
