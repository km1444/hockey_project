from django.contrib import admin

from .models import (
    DescriptionTable, GoalkeeperStatistic, PersonPlayoff, PersonRound2, Player,
    Playoff, Position, Season, Statistic, Team, TeamForTable, TeamForTable2,
    TeamForTable2Round, TeamForTable2Round2, TeamForTable2Round3,
    TeamForTable3, TeamForTable4,
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
    list_display = ('points', 'name', 'current_name', 'season')
    search_fields = ('name__title',)
    list_filter = ('name',)


class TeamForTable2Admin(admin.ModelAdmin):
    list_display = ('points', 'name', 'current_name', 'season')
    search_fields = ('name__title',)
    list_filter = ('name',)


class TeamForTable3Admin(admin.ModelAdmin):
    list_display = ('points', 'name', 'current_name', 'season')
    search_fields = ('name__title',)
    list_filter = ('name',)


class TeamForTable4Admin(admin.ModelAdmin):
    list_display = ('points', 'name', 'current_name', 'season')
    search_fields = ('name__title',)
    list_filter = ('name',)


class TeamForTable2RoundAdmin(admin.ModelAdmin):
    list_display = ('points', 'name', 'current_name', 'season')
    search_fields = ('name',)
    list_filter = ('name',)


class TeamForTable2Round2Admin(admin.ModelAdmin):
    list_display = ('points', 'name', 'current_name', 'season')
    search_fields = ('name',)
    list_filter = ('name',)


class TeamForTable2Round3Admin(admin.ModelAdmin):
    list_display = ('points', 'name', 'current_name', 'season')
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


class GoalkeeperStatisticAdmin(admin.ModelAdmin):
    list_display = ('name', 'season', 'team',)
    search_fields = ('name__name',)
    list_filter = ('name',)
    empty_value_display = '-empty-'


class DescriptionTableAdmin(admin.ModelAdmin):
    list_display = ('season',)
    list_filter = ('season',)


class PersonRound2Admin(admin.ModelAdmin):
    pass


admin.site.register(Team)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Statistic, StatisticAdmin)
admin.site.register(Position)
admin.site.register(Season)
admin.site.register(TeamForTable, TeamForTableAdmin)
admin.site.register(TeamForTable2, TeamForTableAdmin)
admin.site.register(TeamForTable3, TeamForTableAdmin)
admin.site.register(TeamForTable4, TeamForTableAdmin)
admin.site.register(TeamForTable2Round, TeamForTable2RoundAdmin)
admin.site.register(TeamForTable2Round2, TeamForTable2RoundAdmin)
admin.site.register(TeamForTable2Round3, TeamForTable2RoundAdmin)
admin.site.register(Playoff, PlayoffAdmin)
admin.site.register(PersonPlayoff, PersonPlayoffAdmin)
admin.site.register(GoalkeeperStatistic, GoalkeeperStatisticAdmin)
admin.site.register(DescriptionTable, DescriptionTableAdmin)
admin.site.register(PersonRound2, PersonRound2Admin)
