from django.contrib import admin

from .models import (
    PersonPlayoff, Player, Playoff, Position, Season, Statistic, Team,
    TeamForTable, TeamForTable2Round,
)


class StatisticAdmin(admin.ModelAdmin):
    list_display = ('name', 'season', 'team', 'point')
    search_fields = ('name__name',)
    list_filter = ('name',)
    fields = [
        'name', 'team', 'season', 'position',
        ('game', 'goal', 'assist', 'penalty')
    ]
    empty_value_display = '-empty-'


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'year_of_birth')
    search_fields = ('name',)
    list_filter = ('name',)


class TeamForTableAdmin(admin.ModelAdmin):
    list_display = ('points', 'name', 'season')
    search_fields = ('name',)
    list_filter = ('name',)


class TeamForTable2RoundAdmin(admin.ModelAdmin):
    list_display = ('name', 'points')
    search_fields = ('name',)
    list_filter = ('name',)


class PlayoffAdmin(admin.ModelAdmin):
    list_display = ('study', 'result_serie', 'team_1', 'team_2')
    search_fields = ('study',)
    list_filter = ('study',)


class PersonPlayoffAdmin(admin.ModelAdmin):
    list_display = ('result', 'team', 'season')
    search_fields = ('team',)
    list_filter = ('team',)


admin.site.register(Team)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Statistic, StatisticAdmin)
admin.site.register(Position)
admin.site.register(Season)
admin.site.register(TeamForTable, TeamForTableAdmin)
admin.site.register(TeamForTable2Round, TeamForTable2RoundAdmin)
admin.site.register(Playoff, PlayoffAdmin)
admin.site.register(PersonPlayoff, PersonPlayoffAdmin)
