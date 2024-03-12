from django.db import models
from rating.models import Player, Season, Team


class CoachStatistic(models.Model):
    name = models.ForeignKey(
        Player,
        verbose_name="Игрок",
        on_delete=models.CASCADE,
        related_name='coachstatistic'
    )
    age = models.SmallIntegerField('Возраст', default=14)
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='coachstatistic',
        verbose_name="Команда"
    )
    season = models.ForeignKey(
        Season,
        verbose_name='Сезон',
        on_delete=models.CASCADE,
        related_name='coachstatistic'
    )
    final_position = models.SmallIntegerField(
        blank=True,
        null=True,
    )
    full_season = models.BooleanField(default=True)
    fired_season = models.BooleanField(default=False)
    came_season = models.BooleanField(default=False)

    @property
    def get_age(self):
        year_of_birth_player = self.name.year_of_birth
        season = int(self.season.name[:4])
        return season - year_of_birth_player

    def save(self, *args, **kwargs):
        self.age = self.get_age
        super(CoachStatistic, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Статистика тренера'
        verbose_name_plural = 'Статистика тренеров'
        constraints = [
            models.UniqueConstraint(
                name='unique_coach_statistic',
                fields=['name', 'team', 'season']
            )
        ]
        ordering = ('-season',)
