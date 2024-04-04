from django.contrib import admin

from .models import CoachStatistic


class CoachStatisticAdmin(admin.ModelAdmin):
    list_display = ('coach_name', 'season', 'team')
    search_fields = ('coach_name__name',)
    list_filter = ('coach_name',)
    fields = [
        'coach_name', 'team', 'season', 'final_position',
        'full_season', 'fired_season', 'came_season'
    ]
    empty_value_display = '-empty-'


admin.site.register(CoachStatistic, CoachStatisticAdmin)
