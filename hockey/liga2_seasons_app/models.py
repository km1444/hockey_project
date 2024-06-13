from django.db import models
from rating.models import Player, Season, Team


class TransitionSerie(models.Model):
    team_1 = models.ForeignKey(
        Team,
        verbose_name="Команда",
        on_delete=models.CASCADE,
        related_name='team1_in_transserie'
    )
    team_2 = models.ForeignKey(
        Team,
        verbose_name="Команда",
        on_delete=models.CASCADE,
        related_name='team2_in_transserie'
    )
    game_1 = models.CharField("Счет матча 1", max_length=10)
    game_2 = models.CharField("Счет матча 2", max_length=10)
    game_3 = models.CharField("Счет матча 3", max_length=10)
    game_4 = models.CharField("Счет матча 4", max_length=10)


class TransitionWithoutPoints(models.Model):
    rank = models.IntegerField("Место в таблице")
    team_name = models.ForeignKey(
        Team,
        verbose_name="Команда",
        null=True,
        on_delete=models.CASCADE)
    current_name = models.CharField("Текущее имя", max_length=50)
    season = models.ForeignKey(
        Season,
        verbose_name='Сезон',
        on_delete=models.CASCADE,
        related_name='without_points'
    )
    games = models.IntegerField()
    wins = models.IntegerField()
    ties = models.IntegerField()
    losses = models.IntegerField()
    points = models.IntegerField(default=0)

    @property
    def get_points(self):
        score = self.wins * 2 + self.ties
        return score

    def save(self, *args, **kwargs):
        self.points = self.get_points
        super(TransitionWithoutPoints, self).save(*args, **kwargs)

    class Meta:
        verbose_name = (
            "Команда переходного турнира без ранее набранных очков")
        verbose_name_plural = (
            "Команды переходного турнира без ранее набранных очков")

    def __str__(self):
        return f'{self.team_name}, {self.season}'


class TransitionTournament(models.Model):
    rank_real = models.IntegerField("Место для формирования таблицы")
    rank_pict = models.IntegerField("Место выводимое на экран")
    team_name = models.ForeignKey(
        Team,
        verbose_name="Команда",
        null=True,
        on_delete=models.CASCADE)
    current_name = models.CharField("Текущее имя", max_length=50)
    season = models.ForeignKey(
        Season,
        verbose_name='Сезон',
        on_delete=models.CASCADE,
        related_name='team_in_transtour'
    )
    games = models.IntegerField()
    wins = models.IntegerField()
    ties = models.IntegerField()
    losses = models.IntegerField()
    points = models.IntegerField(default=0)

    @property
    def get_points(self):
        score = self.wins * 2 + self.ties
        return score

    def save(self, *args, **kwargs):
        self.points = self.get_points
        super(TransitionTournament, self).save(*args, **kwargs)

    class Meta:
        verbose_name = ("Команда переходного турнира")
        verbose_name_plural = ("Команды переходного турнира")

    def __str__(self):
        return f'{self.team_name}, {self.season}'

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})


class TeamInTable1gr(models.Model):
    rank = models.IntegerField('Место')
    team_name = models.ForeignKey(
        Team,
        null=True,
        on_delete=models.CASCADE,
        related_name='team_in_tables',
        verbose_name="Команда"
    )
    current_name = models.CharField(
        ("Текущее название"), max_length=50, blank=True)
    season = models.ForeignKey(
        Season,
        verbose_name='Сезон',
        on_delete=models.CASCADE,
        related_name='team_in_tables'
    )
    games = models.IntegerField()
    wins = models.IntegerField()
    ties = models.IntegerField()
    losses = models.IntegerField()
    points = models.IntegerField(default=0)
    coach_1 = models.ForeignKey(
        Player,
        verbose_name='Тренер',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='team_in_tables_coach_1',)
    coach_2 = models.ForeignKey(
        Player,
        verbose_name='Тренер_2',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='team_in_tables_coach_2')
    coach_3 = models.ForeignKey(
        Player,
        verbose_name='Тренер_3',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='team_in_tables_coach_3')
    transition_tournament = models.ForeignKey(
        TransitionTournament,
        verbose_name="Участие в переходном турнире",
        blank=True,
        null=True,
        on_delete=models.SET_NULL)
    transition_tournament_without_points = models.ForeignKey(
        TransitionWithoutPoints,
        verbose_name="Участие в перех т-ре без учета ранее набранных очков",
        blank=True,
        null=True,
        on_delete=models.SET_NULL)
    transition_serie = models.ForeignKey(
        TransitionSerie,
        verbose_name="Участие в переходной серии",
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    additional_tournament = models.ForeignKey(
        'AdditionalTournament',
        verbose_name="Участие в доп.турнире",
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    additional_tournament_second = models.ForeignKey(
        'AdditionalTournamentSecond',
        verbose_name="Участие во втором доп.турнире",
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    additional_tournament_without_points = models.ForeignKey(
        'AdditionalTournamentWithoutPoints',
        verbose_name="Участие в доп т-ре без учета ранее набранных очков",
        blank=True,
        null=True,
        on_delete=models.SET_NULL)

    @property
    def get_points(self):
        score = self.wins * 2 + self.ties
        return score

    def save(self, *args, **kwargs):
        self.points = self.get_points
        super(TeamInTable1gr, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Команда 1 группы"
        verbose_name_plural = "Команды 1 группы"
        ordering = ('season__name',)

    def __str__(self):
        return f'{self.team_name}, {self.season}'


class TeamInTable2gr(models.Model):
    rank = models.IntegerField('Место')
    team_name = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='team_in_2_tables',
        verbose_name="Команда"
    )
    current_name = models.CharField(
        ("Текущее название"), max_length=50, blank=True)
    season = models.ForeignKey(
        Season,
        verbose_name='Сезон',
        on_delete=models.CASCADE,
        related_name='team_in_2_tables'
    )
    games = models.IntegerField()
    wins = models.IntegerField()
    ties = models.IntegerField()
    losses = models.IntegerField()
    points = models.IntegerField(default=0)
    coach_1 = models.ForeignKey(
        Player,
        verbose_name='Тренер',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='team_in_2_tables_coach_1',
    )
    coach_2 = models.ForeignKey(
        Player,
        verbose_name='Тренер_2',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='team_in_2_tables_coach_2'
    )
    coach_3 = models.ForeignKey(
        Player,
        verbose_name='Тренер_3',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='team_in_2_tables_coach_3'
    )
    transition_tournament = models.OneToOneField(
        TransitionTournament,
        verbose_name="Участие в переходном турнире",
        blank=True,
        null=True,
        on_delete=models.SET_NULL)
    transition_tournament_without_points = models.ForeignKey(
        TransitionWithoutPoints,
        verbose_name="Участие в перех т-ре без учета ранее набранных очков",
        blank=True,
        null=True,
        on_delete=models.SET_NULL)
    transition_serie = models.ForeignKey(
        TransitionSerie,
        verbose_name="Участие в переходной серии",
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    additional_tournament = models.ForeignKey(
        'AdditionalTournament',
        verbose_name="Участие в доп.турнире",
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    additional_tournament_second = models.ForeignKey(
        'AdditionalTournamentSecond',
        verbose_name="Участие во втором доп.турнире",
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    additional_tournament_without_points = models.ForeignKey(
        'AdditionalTournamentWithoutPoints',
        verbose_name="Участие в доп т-ре без учета ранее набранных очков",
        blank=True,
        null=True,
        on_delete=models.SET_NULL)

    @property
    def get_points(self):
        score = self.wins * 2 + self.ties
        return score

    def save(self, *args, **kwargs):
        self.points = self.get_points
        super(TeamInTable2gr, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Команда второй группы"
        verbose_name_plural = "Команды второй группы"
        ordering = ('season__name',)

    def __str__(self):
        return f'{self.team_name}, {self.season}'


class AdditionalTournament(models.Model):
    rank = models.IntegerField('Место')
    team_name = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='team_in_add_tables',
        verbose_name="Команда"
    )
    current_name = models.CharField(
        ("Текущее название"),
        max_length=50
    )
    season = models.ForeignKey(
        Season,
        verbose_name='Сезон',
        on_delete=models.CASCADE,
        related_name='team_in_add_tables'
    )
    games = models.IntegerField()
    wins = models.IntegerField()
    ties = models.IntegerField()
    losses = models.IntegerField()
    points = models.IntegerField(default=0)

    @property
    def get_points(self):
        score = self.wins * 2 + self.ties
        return score

    def save(self, *args, **kwargs):
        self.points = self.get_points
        super(AdditionalTournament, self).save(*args, **kwargs)

    class Meta:
        verbose_name = ("Команда дополнителного турнира")
        verbose_name_plural = ("Команды дополнительного турнира")

    def __str__(self):
        return f'{self.team_name}, {self.season}'


class AdditionalTournamentSecond(models.Model):
    rank = models.IntegerField('Место')
    team_name = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='team_in_add_tables_2',
        verbose_name="Команда"
    )
    current_name = models.CharField(
        ("Текущее название"),
        max_length=50
    )
    season = models.ForeignKey(
        Season,
        verbose_name='Сезон',
        on_delete=models.CASCADE,
        related_name='team_in_add_tables_2'
    )
    games = models.IntegerField()
    wins = models.IntegerField()
    ties = models.IntegerField()
    losses = models.IntegerField()
    points = models.IntegerField(default=0)

    @property
    def get_points(self):
        score = self.wins * 2 + self.ties
        return score

    def save(self, *args, **kwargs):
        self.points = self.get_points
        super(AdditionalTournamentSecond, self).save(*args, **kwargs)

    class Meta:
        verbose_name = ("Команда второго дополнителного турнира")
        verbose_name_plural = ("Команды второго дополнительного турнира")

    def __str__(self):
        return f'{self.team_name}, {self.season}'


class AdditionalTournamentWithoutPoints(models.Model):
    rank = models.IntegerField('Место')
    team_name = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='additional_tournament_without_points',
        verbose_name="Команда"
    )
    current_name = models.CharField(
        ("Текущее название"),
        max_length=50
    )
    season = models.ForeignKey(
        Season,
        verbose_name='Сезон',
        on_delete=models.CASCADE,
        related_name='additional_tournament_without_points'
    )
    games = models.IntegerField()
    wins = models.IntegerField()
    ties = models.IntegerField()
    losses = models.IntegerField()
    points = models.IntegerField(default=0)

    @property
    def get_points(self):
        score = self.wins * 2 + self.ties
        return score

    def save(self, *args, **kwargs):
        self.points = self.get_points
        super(AdditionalTournamentWithoutPoints, self).save(*args, **kwargs)

    class Meta:
        verbose_name = ("Команда доп т-ра без учета набранных ранее очков")
        verbose_name_plural = (
            "Команды доп т-ра без учета набранных ранее очков")

    def __str__(self):
        return f'{self.team_name}, {self.season}'


class DescriptionTable(models.Model):
    season = models.ForeignKey(
        Season,
        verbose_name='Сезон',
        on_delete=models.CASCADE,
        related_name='description_table_liga2'
    )
    transition_tournament = models.CharField(
        'Переходный турнир', blank=True, max_length=50)
    description_1tb = models.CharField(
        'Основной турнир или Запад', blank=True, max_length=50)
    description_2tb = models.CharField(
        'Дополнительный турнир', blank=True, max_length=50)
    description_3tb = models.CharField(
        'Второй доп турнир', blank=True, max_length=50)
    description_4tb = models.CharField(
        'Восток', blank=True, max_length=50)

    def __str__(self):
        return f'{self.season}'
