from django.db import models


class Team(models.Model):
    emblem = models.ImageField(
        'Эмблема',
        upload_to='emblem/',
        blank=True
    )
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
    name = models.TextField("Игрок")
    year_of_birth = models.SmallIntegerField("Год рождения")
    wikip = models.URLField("Ссылка на википедию", blank=True, max_length=250)

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
    name = models.CharField('Название сезона', max_length=10)
    description = models.TextField('Описание сезона', blank=True)

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
        default=1,
        related_name='statistics',
        verbose_name="Команда"
    )
    season = models.ForeignKey(
        Season,
        verbose_name='Сезон',
        on_delete=models.CASCADE,
        default=1,
        related_name='statistics'
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        default=2,
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
        verbose_name = 'Статистика полевого игрока'
        verbose_name_plural = 'Статистика полевых игроков'
        constraints = [
            models.UniqueConstraint(
                name='unique_statistic',
                fields=['name', 'team', 'season']
            )
        ]
        ordering = ('-season',)


class GoalkeeperStatistic(models.Model):
    name = models.ForeignKey(
        Player,
        verbose_name="Игрок",
        on_delete=models.CASCADE,
        default=1,
        related_name='goalkeeperstatistic'
    )
    age = models.SmallIntegerField('Возраст', default=14)
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        default=1,
        related_name='goalkeeperstatistic',
        verbose_name="Команда"
    )
    season = models.ForeignKey(
        Season,
        verbose_name='Сезон',
        default=1,
        on_delete=models.CASCADE,
        related_name='goalkeeperstatistic'
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        default=3,
        blank=True,
        null=True,
        related_name='goalkeeperstatistic',
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
        super(GoalkeeperStatistic, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Статистика Вратаря"
        verbose_name_plural = "Статистика Вратарей"
        constraints = [
            models.UniqueConstraint(
                name='unique_goalkeeper_statistic',
                fields=['name', 'team', 'season']
            )
        ]
        ordering = ('-season',)


class Playoff(models.Model):
    """модель для заполнения сетки плейофф"""
    number = models.IntegerField('Номер серии')
    season = models.ForeignKey(
        Season,
        verbose_name='Сезон',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='playoff'
    )
    study = models.CharField('Стадия', max_length=10)
    result_serie = models.CharField('Результат серии', max_length=4)
    team_1 = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='playoff_1',
        verbose_name="Команда_1"
    )
    current_name_team_1 = models.CharField(
        ("Текущее название"), max_length=50, blank=True)
    team_2 = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='playoff_2',
        verbose_name="Команда_2"
    )
    current_name_team_2 = models.CharField(
        ("Текущее название"), max_length=50, blank=True)

    class Meta:
        verbose_name = ("Серия")
        verbose_name_plural = ("Серии")


class PersonPlayoff(models.Model):
    """модель с результатами плейофф команды"""
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='person_playoff',
    )
    season = models.ForeignKey(
        Season,
        verbose_name='Сезон',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='person_playoff'
    )
    result = models.CharField('Стадия', max_length=20)

    def __str__(self):
        return self.result


class TeamForTable2Round(models.Model):
    rank = models.IntegerField('Место')
    name = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='team_for_tables_2_round',
        verbose_name="Команда"
    )
    current_name = models.CharField(
        ("Текущее название"), max_length=50, blank=True)
    season = models.ForeignKey(
        Season,
        verbose_name='Сезон',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='team_for_tables_2_round'
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
        super(TeamForTable2Round, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Команда 1 группы 2 раунда"
        verbose_name_plural = "Команды 1 группы 2 раунда"
        ordering = ('season__name',)

    def __str__(self):
        return f'{self.name}, {self.season}'


class TeamForTable2Round2(models.Model):
    rank = models.IntegerField('Место')
    name = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='team_for_tables_2_round2',
        verbose_name="Команда"
    )
    current_name = models.CharField(
        ("Текущее название"), max_length=50, blank=True)
    season = models.ForeignKey(
        Season,
        verbose_name='Сезон',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='team_for_tables_2_round2'
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
        super(TeamForTable2Round2, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Команда 2 группы 2 раунда"
        verbose_name_plural = "Команды 2 группы 2 раунда"
        ordering = ('season__name',)

    def __str__(self):
        return f'{self.name}, {self.season}'


class TeamForTable2Round3(models.Model):
    rank = models.IntegerField('Место')
    name = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='team_for_tables_2_round3',
        verbose_name="Команда"
    )
    current_name = models.CharField(
        ("Текущее название"), max_length=50, blank=True)
    season = models.ForeignKey(
        Season,
        verbose_name='Сезон',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='team_for_tables_2_round3'
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
        super(TeamForTable2Round3, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Команда 3 группы 2 раунда"
        verbose_name_plural = "Команды 3 группы 2 раунда"
        ordering = ('season__name',)

    def __str__(self):
        return f'{self.name}, {self.season}'


class PersonRound2(models.Model):
    table1 = models.ForeignKey(
        TeamForTable2Round,
        verbose_name=(""),
        on_delete=models.CASCADE,
        blank=True,
        null=True,)
    table2 = models.ForeignKey(
        TeamForTable2Round2,
        verbose_name=(""),
        on_delete=models.CASCADE,
        blank=True,
        null=True,)
    table3 = models.ForeignKey(
        TeamForTable2Round3,
        verbose_name=(""),
        on_delete=models.CASCADE,
        blank=True,
        null=True,)


class TeamForTable(models.Model):
    rank = models.IntegerField('Место')
    round_2 = models.ForeignKey(
        PersonRound2,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='team_for_tables',
    )
    playoff = models.ForeignKey(
        PersonPlayoff,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='team_for_tables',
    )
    name = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='team_for_tables',
        verbose_name="Команда"
    )
    current_name = models.CharField(
        ("Текущее название"), max_length=50, blank=True)
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
    coach = models.CharField("Тренер", max_length=50, blank=True)

    @property
    def get_points_percentage(self):
        max_point = self.games * 2
        return round((self.points / max_point * 100), 1)

    def save(self, *args, **kwargs):
        self.points_percentage = self.get_points_percentage
        super(TeamForTable, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Команда основной или 1 группы 1 раунда"
        verbose_name_plural = "Команды основной или 1 группы 1 раунда"
        ordering = ('season__name',)

    def __str__(self):
        return f'{self.name}, {self.season}'


class TeamForTable2(models.Model):
    rank = models.IntegerField('Место')
    round_2 = models.ForeignKey(
        PersonRound2,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='team_for_tables2',
    )
    playoff = models.ForeignKey(
        PersonPlayoff,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='team_for_tables2',
    )
    name = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='team_for_tables2',
        verbose_name="Команда"
    )
    current_name = models.CharField(
        ("Текущее название"), max_length=50, blank=True)
    season = models.ForeignKey(
        Season,
        verbose_name='Сезон',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='team_for_tables2'
    )
    games = models.IntegerField()
    wins = models.IntegerField()
    ties = models.IntegerField()
    losses = models.IntegerField()
    points = models.IntegerField()
    points_percentage = models.FloatField(default=0)
    goals_for = models.IntegerField()
    goals_against = models.IntegerField()
    coach = models.CharField("Тренер", max_length=50, blank=True)

    @property
    def get_points_percentage(self):
        max_point = self.games * 2
        return round((self.points / max_point * 100), 1)

    def save(self, *args, **kwargs):
        self.points_percentage = self.get_points_percentage
        super(TeamForTable2, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Команда 2 группы 1 раунда"
        verbose_name_plural = "Команды 2 группы 1 раунда"
        ordering = ('season__name',)

    def __str__(self):
        return f'{self.name}, {self.season}'


class TeamForTable3(models.Model):
    rank = models.IntegerField('Место')
    round_2 = models.ForeignKey(
        PersonRound2,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='team_for_tables3',
    )
    playoff = models.ForeignKey(
        PersonPlayoff,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='team_for_tables3',
    )
    name = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='team_for_tables3',
        verbose_name="Команда"
    )
    current_name = models.CharField(
        ("Текущее название"), max_length=50, blank=True)
    season = models.ForeignKey(
        Season,
        verbose_name='Сезон',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='team_for_tables3'
    )
    games = models.IntegerField()
    wins = models.IntegerField()
    ties = models.IntegerField()
    losses = models.IntegerField()
    points = models.IntegerField()
    points_percentage = models.FloatField(default=0)
    goals_for = models.IntegerField()
    goals_against = models.IntegerField()
    coach = models.CharField("Тренер", max_length=50, blank=True)

    @property
    def get_points_percentage(self):
        max_point = self.games * 2
        return round((self.points / max_point * 100), 1)

    def save(self, *args, **kwargs):
        self.points_percentage = self.get_points_percentage
        super(TeamForTable3, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Команда 3 группы 1 раунда"
        verbose_name_plural = "Команды 3 группы 1 раунда"
        ordering = ('season__name',)

    def __str__(self):
        return f'{self.name}, {self.season}'


class TeamForTable4(models.Model):
    rank = models.IntegerField('Место')
    round_2 = models.ForeignKey(
        PersonRound2,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='team_for_tables4',
    )
    playoff = models.ForeignKey(
        PersonPlayoff,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='team_for_tables4',
    )
    name = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='team_for_tables4',
        verbose_name="Команда"
    )
    current_name = models.CharField(
        ("Текущее название"), max_length=50, blank=True)
    season = models.ForeignKey(
        Season,
        verbose_name='Сезон',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='team_for_tables4'
    )
    games = models.IntegerField()
    wins = models.IntegerField()
    ties = models.IntegerField()
    losses = models.IntegerField()
    points = models.IntegerField()
    points_percentage = models.FloatField(default=0)
    goals_for = models.IntegerField()
    goals_against = models.IntegerField()
    coach = models.CharField("Тренер", max_length=50, blank=True)

    @property
    def get_points_percentage(self):
        max_point = self.games * 2
        return round((self.points / max_point * 100), 1)

    def save(self, *args, **kwargs):
        self.points_percentage = self.get_points_percentage
        super(TeamForTable4, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Команда 4 группы 1 раунда"
        verbose_name_plural = "Команды 4 группы 1 раунда"
        ordering = ('season__name',)

    def __str__(self):
        return f'{self.name}, {self.season}'


class DescriptionTable(models.Model):
    season = models.ForeignKey(
        Season,
        verbose_name='Сезон',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='description_table'
    )
    description_playoff = models.CharField(
        'Название плейофф', blank=True, max_length=50)
    description_1gr_2round = models.CharField(
        'Название таблицы 1гр 2 р', blank=True, max_length=50)
    description_2gr_2round = models.CharField(
        'Название таблицы 2 гр 2 р', blank=True, max_length=50)
    description_3gr_2round = models.CharField(
        'Название таблицы 3 гр 2 р', blank=True, max_length=50)
    description_1gr_1round = models.CharField(
        'Название таблицы 1 гр 1 р', blank=True, max_length=50)
    description_2gr_1round = models.CharField(
        'Название таблицы 2 гр 1 р', blank=True, max_length=50)
    description_3gr_1round = models.CharField(
        'Название таблицы 3 гр 1 р', blank=True, max_length=50)
    description_4gr_1round = models.CharField(
        'Название таблицы 4 гр 1 р', blank=True, max_length=50)
