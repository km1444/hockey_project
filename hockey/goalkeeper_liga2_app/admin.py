from django.contrib import admin

from .models import GoalkeeperStatisticLiga2


@admin.register(GoalkeeperStatisticLiga2)
class GoalkeeperStatisticLiga2Admin(admin.ModelAdmin):
    list_display = ('name', 'season', 'team',)
    search_fields = ('name__name',)
    list_filter = ('name',)
    empty_value_display = '-empty-'
