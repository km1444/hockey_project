from django.db import models
from rating.models import Player, Position, Season, Team


class StatisticPlayer(models.Model):
    name = models.ForeignKey(
        Player,
        verbose_name="Игрок",
        on_delete=models.CASCADE,
        related_name='statistics_player'
    )
    age = models.SmallIntegerField('Возраст', default=14)
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        default=1,
        related_name='statistics_player',
        verbose_name="Команда"
    )
    season = models.ForeignKey(
        Season,
        verbose_name='Сезон',
        on_delete=models.CASCADE,
        default=1,
        related_name='statistics_player'
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        default=2,
        blank=True,
        null=True,
        related_name='statistics_player',
        verbose_name="Позиция"
    )
    game = models.SmallIntegerField("Игры", default=1)
    goal = models.SmallIntegerField("Голы", default=0)
    assist = models.SmallIntegerField("Передачи", default=0)
    point = models.SmallIntegerField("Очки", default=0)
    penalty = models.SmallIntegerField("Штраф", default=0)

    @property
    def get_point(self):
        goal = self.goal
        assist = self.assist
        return goal + assist

    @property
    def get_age(self):
        year_of_birth_player = self.name.year_of_birth
        season = int(self.season.name[:4])
        return season - year_of_birth_player

    def save(self, *args, **kwargs):
        self.point = self.get_point
        self.age = self.get_age
        super(StatisticPlayer, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Статистика полевого игрока'
        verbose_name_plural = 'Статистика полевых игроков'
        constraints = [
            models.UniqueConstraint(
                name='unique_statistic_players',
                fields=['name', 'team', 'season']
            )
        ]
        ordering = ('-season',)
