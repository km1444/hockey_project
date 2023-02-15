from django.contrib import admin

from .models import Player, Position, Season, Statistic, Team


class StatisticAdmin(admin.ModelAdmin):
    # Перечисляем поля, которые должны отображаться в админке
    list_display = ('name', 'season', 'team', 'point')
    # Добавляем интерфейс для поиска по тексту постов
    search_fields = ('name',)
    # Добавляем возможность фильтрации по дате
    list_filter = ('name',)


class PlayerAdmin(admin.ModelAdmin):
    # Перечисляем поля, которые должны отображаться в админке
    list_display = ('name', 'year_of_birth')
    # Добавляем интерфейс для поиска по тексту постов
    search_fields = ('name',)
    # Добавляем возможность фильтрации по дате
    list_filter = ('name',)


admin.site.register(Team)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Statistic, StatisticAdmin)
admin.site.register(Position)
admin.site.register(Season)
