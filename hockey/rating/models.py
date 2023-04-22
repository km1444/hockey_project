from django.db import models


class Team(models.Model):
    title = models.CharField("Название команды", max_length=200)
    city = models.CharField("Город", max_length=100, blank=True)
    slug = models.SlugField("Уникальное имя", max_length=100, unique=True)
    # description = models.TextField("Описание")

    def natural_key(self):
        return (self.title)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"


class Player(models.Model):
    name = models.TextField("Текст")
    year_of_birth = models.SmallIntegerField("Год рождения")

    def natural_key(self):
        return (self.name)

    def __str__(self):
        return f'{self.name} {self.year_of_birth}'
        # return self.name

    class Meta:
        verbose_name = "Игрок"
        verbose_name_plural = "Игроки"
        constraints = [
            models.UniqueConstraint(
                name='unique_player',
                fields=['name', 'year_of_birth']
            )
        ]


class Position(models.Model):
    name = models.TextField('Текст')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Позиция"
        verbose_name_plural = "Позиции"


class Season(models.Model):
    name = models.TextField('Текст')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Сезон"
        verbose_name_plural = "Сезоны"


class Statistic(models.Model):
    name = models.ForeignKey(
        Player,
        verbose_name="Игрок",
        on_delete=models.CASCADE,
        related_name='statistics'
    )
    age = models.SmallIntegerField('Возраст', default=14)
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        default=13,
        blank=True,
        null=True,
        related_name='statistics',
        verbose_name="Команда"
    )
    season = models.ForeignKey(
        Season,
        verbose_name='Сезон',
        on_delete=models.CASCADE,
        default=11,
        related_name='statistics'
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        default=1,
        blank=True,
        null=True,
        related_name='statistics',
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
        super(Statistic, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Статистика"
        verbose_name_plural = "Статистика"
        ordering = ('-point', '-goal', 'game')


class Team_for_table(models.Model):
    rank = models.IntegerField('Место')
    name = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='team_for_tables',
        verbose_name="Команда"
    )
    season = models.ForeignKey(
        Season,
        verbose_name='Сезон',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='team_for_tables'
    )
    games = models.IntegerField()
    wins = models.IntegerField()
    ties = models.IntegerField()
    losses = models.IntegerField()
    points = models.IntegerField()
    points_percentage = models.FloatField(default=0)
    goals_for = models.IntegerField()
    goals_against = models.IntegerField()

    @property
    def get_points_percentage(self):
        max_point = self.games * 2
        return round((self.points / max_point * 100), 1)

    def save(self, *args, **kwargs):
        self.points_percentage = self.get_points_percentage
        super(Team_for_table, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-points_percentage',)
