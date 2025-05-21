from django.contrib import admin

from .models import (
    AdditionalTournament, AdditionalTournamentSecond,
    AdditionalTournamentWithoutPoints, AdditionalTournamentWithoutPointsSecond,
    DescriptionTable, TeamInTable1gr, TeamInTable2gr, TransitionTournament,
    TransitionWithoutPoints,
)


class TransitionWithoutPointsAdmin(admin.ModelAdmin):
    list_display = ('points', 'team_name', 'current_name', 'season')
    search_fields = ('team_name__title',)
    list_filter = ('team_name',)


class TransitionTournamentAdmin(admin.ModelAdmin):
    list_display = ('points', 'team_name', 'current_name', 'season')
    search_fields = ('team_name__title',)
    list_filter = ('team_name',)


class TeamInTable1grAdmin(admin.ModelAdmin):
    list_display = ('points', 'team_name', 'current_name', 'season')
    search_fields = ('team_name__title',)
    list_filter = ('team_name',)


class TeamInTable2grAdmin(admin.ModelAdmin):
    list_display = ('points', 'team_name', 'current_name', 'season')
    search_fields = ('team_name__title',)
    list_filter = ('team_name',)


class AdditionalTournamentAdmin(admin.ModelAdmin):
    list_display = ('points', 'team_name', 'current_name', 'season')
    search_fields = ('team_name__title',)
    list_filter = ('team_name',)


class AdditionalTournamentSecondAdmin(admin.ModelAdmin):
    list_display = ('points', 'team_name', 'current_name', 'season')
    search_fields = ('team_name__title',)
    list_filter = ('team_name',)


class AdditionalTournamentWithoutPointsAdmin(admin.ModelAdmin):
    list_display = ('points', 'team_name', 'current_name', 'season')
    search_fields = ('team_name__title',)
    list_filter = ('team_name',)


class AdditionalTournamentWithoutPointsSecondAdmin(admin.ModelAdmin):
    list_display = ('points', 'team_name', 'current_name', 'season')
    search_fields = ('team_name__title',)
    list_filter = ('team_name',)


class DescriptionTableAdmin(admin.ModelAdmin):
    list_display = ('season',)
    list_filter = ('season',)


admin.site.register(TransitionTournament, TransitionTournamentAdmin)
admin.site.register(TransitionWithoutPoints, TransitionWithoutPointsAdmin)
admin.site.register(TeamInTable1gr, TeamInTable1grAdmin)
admin.site.register(TeamInTable2gr, TeamInTable2grAdmin)
admin.site.register(AdditionalTournament, AdditionalTournamentAdmin)
admin.site.register(
    AdditionalTournamentSecond,
    AdditionalTournamentSecondAdmin
)
admin.site.register(
    AdditionalTournamentWithoutPoints,
    AdditionalTournamentWithoutPointsAdmin
)
admin.site.register(
    AdditionalTournamentWithoutPointsSecond,
    AdditionalTournamentWithoutPointsSecondAdmin
)
admin.site.register(DescriptionTable, DescriptionTableAdmin)
