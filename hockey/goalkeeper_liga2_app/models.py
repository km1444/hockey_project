from django.db import models
from rating.models import Player, Position, Season, Team


class GoalkeeperStatisticLiga2(models.Model):
    name = models.ForeignKey(
        Player,
        verbose_name="Игрок",
        on_delete=models.CASCADE,
        default=1,
        related_name='goalkeeperstatistic_liga2'
    )
    age = models.SmallIntegerField('Возраст', default=14)
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        default=1,
        related_name='goalkeeperstatistic_liga2',
        verbose_name="Команда"
    )
    season = models.ForeignKey(
        Season,
        verbose_name='Сезон',
        default=1,
        on_delete=models.CASCADE,
        related_name='goalkeeperstatistic_liga2'
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        default=3,
        blank=True,
        null=True,
        related_name='goalkeeperstatistic_liga2',
        verbose_name="Позиция"
    )
    game = models.SmallIntegerField("Игры", default=1)
    goal_against = models.SmallIntegerField("Голы", default=0)
    penalty = models.SmallIntegerField("Штраф", default=0)

    @property
    def get_age(self):
        year_of_birth_player = self.name.year_of_birth
        season = int(self.season.name[:4])
        return season - year_of_birth_player

    def save(self, *args, **kwargs):
        self.age = self.get_age
        super(GoalkeeperStatisticLiga2, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Статистика Вратаря в первой лиге"
        verbose_name_plural = "Статистика Вратарей в первой лиге"
        constraints = [
            models.UniqueConstraint(
                name='unique_goalkeeper_statistic_liga2',
                fields=['name', 'team', 'season']
            )
        ]
        ordering = ('-season',)
