# Generated by Django 2.2.16 on 2023-07-16 12:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0026_teamfortable_playoff'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonPlayoff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(max_length=20, verbose_name='Стадия')),
                ('season', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='person_playoff', to='rating.Season', verbose_name='Сезон')),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='person_playoff', to='rating.Team')),
            ],
        ),
        migrations.AlterModelOptions(
            name='teamfortable',
            options={'ordering': ('season__name',), 'verbose_name': 'Команда основной или 1 группы 1 раунда', 'verbose_name_plural': 'Команды основной или 1 группы 1 раунда'},
        ),
        migrations.AlterModelOptions(
            name='teamfortable2round',
            options={'ordering': ('-points_percentage',), 'verbose_name': 'Команда 1 группы 2 раунда', 'verbose_name_plural': 'Команды 1 группы 2 раунда'},
        ),
        migrations.AddField(
            model_name='playoff',
            name='current_name_team_1',
            field=models.CharField(blank=True, max_length=50, verbose_name='Текущее название'),
        ),
        migrations.AddField(
            model_name='playoff',
            name='current_name_team_2',
            field=models.CharField(blank=True, max_length=50, verbose_name='Текущее название'),
        ),
        migrations.AddField(
            model_name='teamfortable',
            name='current_name',
            field=models.CharField(blank=True, max_length=50, verbose_name='Текущее название'),
        ),
        migrations.AddField(
            model_name='teamfortable2round',
            name='current_name',
            field=models.CharField(blank=True, max_length=50, verbose_name='Текущее название'),
        ),
        migrations.AlterField(
            model_name='statistic',
            name='season',
            field=models.ForeignKey(default=21, on_delete=django.db.models.deletion.CASCADE, related_name='statistics', to='rating.Season', verbose_name='Сезон'),
        ),
        migrations.AlterField(
            model_name='statistic',
            name='team',
            field=models.ForeignKey(blank=True, default=8, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='statistics', to='rating.Team', verbose_name='Команда'),
        ),
        migrations.AlterField(
            model_name='teamfortable',
            name='playoff',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_for_tables', to='rating.PersonPlayoff'),
        ),
        migrations.AlterField(
            model_name='teamfortable',
            name='round_2',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_for_tables', to='rating.TeamForTable2Round'),
        ),
        migrations.CreateModel(
            name='TeamForTable4',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField(verbose_name='Место')),
                ('current_name', models.CharField(blank=True, max_length=50, verbose_name='Текущее название')),
                ('games', models.IntegerField()),
                ('wins', models.IntegerField()),
                ('ties', models.IntegerField()),
                ('losses', models.IntegerField()),
                ('points', models.IntegerField()),
                ('points_percentage', models.FloatField(default=0)),
                ('goals_for', models.IntegerField()),
                ('goals_against', models.IntegerField()),
                ('coach', models.CharField(blank=True, max_length=50, verbose_name='Тренер')),
                ('name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_for_tables4', to='rating.Team', verbose_name='Команда')),
                ('playoff', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_for_tables4', to='rating.PersonPlayoff')),
                ('round_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_for_tables4', to='rating.TeamForTable2Round')),
                ('season', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_for_tables4', to='rating.Season', verbose_name='Сезон')),
            ],
            options={
                'verbose_name': 'Команда 4 группы 1 раунда',
                'verbose_name_plural': 'Команды 4 группы 1 раунда',
                'ordering': ('season__name',),
            },
        ),
        migrations.CreateModel(
            name='TeamForTable3',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField(verbose_name='Место')),
                ('current_name', models.CharField(blank=True, max_length=50, verbose_name='Текущее название')),
                ('games', models.IntegerField()),
                ('wins', models.IntegerField()),
                ('ties', models.IntegerField()),
                ('losses', models.IntegerField()),
                ('points', models.IntegerField()),
                ('points_percentage', models.FloatField(default=0)),
                ('goals_for', models.IntegerField()),
                ('goals_against', models.IntegerField()),
                ('coach', models.CharField(blank=True, max_length=50, verbose_name='Тренер')),
                ('name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_for_tables3', to='rating.Team', verbose_name='Команда')),
                ('playoff', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_for_tables3', to='rating.PersonPlayoff')),
                ('round_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_for_tables3', to='rating.TeamForTable2Round')),
                ('season', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_for_tables3', to='rating.Season', verbose_name='Сезон')),
            ],
            options={
                'verbose_name': 'Команда 3 группы 1 раунда',
                'verbose_name_plural': 'Команды 3 группы 1 раунда',
                'ordering': ('season__name',),
            },
        ),
        migrations.CreateModel(
            name='TeamForTable2Round3',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField(verbose_name='Место')),
                ('current_name', models.CharField(blank=True, max_length=50, verbose_name='Текущее название')),
                ('games', models.IntegerField()),
                ('wins', models.IntegerField()),
                ('ties', models.IntegerField()),
                ('losses', models.IntegerField()),
                ('points', models.IntegerField()),
                ('points_percentage', models.FloatField(default=0)),
                ('goals_for', models.IntegerField()),
                ('goals_against', models.IntegerField()),
                ('name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_for_tables_2_round3', to='rating.Team', verbose_name='Команда')),
                ('season', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_for_tables_2_round3', to='rating.Season', verbose_name='Сезон')),
            ],
            options={
                'verbose_name': 'Команда 3 группы 2 раунда',
                'verbose_name_plural': 'Команды 3 группы 2 раунда',
                'ordering': ('-points_percentage',),
            },
        ),
        migrations.CreateModel(
            name='TeamForTable2Round2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField(verbose_name='Место')),
                ('current_name', models.CharField(blank=True, max_length=50, verbose_name='Текущее название')),
                ('games', models.IntegerField()),
                ('wins', models.IntegerField()),
                ('ties', models.IntegerField()),
                ('losses', models.IntegerField()),
                ('points', models.IntegerField()),
                ('points_percentage', models.FloatField(default=0)),
                ('goals_for', models.IntegerField()),
                ('goals_against', models.IntegerField()),
                ('name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_for_tables_2_round2', to='rating.Team', verbose_name='Команда')),
                ('season', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_for_tables_2_round2', to='rating.Season', verbose_name='Сезон')),
            ],
            options={
                'verbose_name': 'Команда 2 группы 2 раунда',
                'verbose_name_plural': 'Команды 2 группы 2 раунда',
                'ordering': ('-points_percentage',),
            },
        ),
        migrations.CreateModel(
            name='TeamForTable2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField(verbose_name='Место')),
                ('current_name', models.CharField(blank=True, max_length=50, verbose_name='Текущее название')),
                ('games', models.IntegerField()),
                ('wins', models.IntegerField()),
                ('ties', models.IntegerField()),
                ('losses', models.IntegerField()),
                ('points', models.IntegerField()),
                ('points_percentage', models.FloatField(default=0)),
                ('goals_for', models.IntegerField()),
                ('goals_against', models.IntegerField()),
                ('coach', models.CharField(blank=True, max_length=50, verbose_name='Тренер')),
                ('name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_for_tables2', to='rating.Team', verbose_name='Команда')),
                ('playoff', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_for_tables2', to='rating.PersonPlayoff')),
                ('round_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_for_tables2', to='rating.TeamForTable2Round')),
                ('season', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_for_tables2', to='rating.Season', verbose_name='Сезон')),
            ],
            options={
                'verbose_name': 'Команда 2 группы 1 раунда',
                'verbose_name_plural': 'Команды 2 группы 1 раунда',
                'ordering': ('season__name',),
            },
        ),
        migrations.CreateModel(
            name='GolkeeperStatistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.SmallIntegerField(default=14, verbose_name='Возраст')),
                ('game', models.SmallIntegerField(default=1, verbose_name='Игры')),
                ('goal_against', models.SmallIntegerField(default=0, verbose_name='Голы')),
                ('penalty', models.SmallIntegerField(default=0, verbose_name='Штраф')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='golkeeperstatistic', to='rating.Player', verbose_name='Игрок')),
                ('position', models.ForeignKey(blank=True, default=3, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='golkeeperstatistic', to='rating.Position', verbose_name='Позиция')),
                ('season', models.ForeignKey(default=21, on_delete=django.db.models.deletion.CASCADE, related_name='golkeeperstatistic', to='rating.Season', verbose_name='Сезон')),
                ('team', models.ForeignKey(blank=True, default=8, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='golkeeperstatistic', to='rating.Team', verbose_name='Команда')),
            ],
            options={
                'verbose_name': 'Статистик Вратаря',
                'verbose_name_plural': 'Статистика Вратарей',
                'ordering': ('game',),
            },
        ),
        migrations.CreateModel(
            name='DescriptionTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description_playoff', models.CharField(blank=True, max_length=50, verbose_name='Название плейофф')),
                ('description_1gr_2round', models.CharField(blank=True, max_length=50, verbose_name='Название таблицы 1гр 2 р')),
                ('description_2gr_2round', models.CharField(blank=True, max_length=50, verbose_name='Название таблицы 2 гр 2 р')),
                ('description_3gr_2round', models.CharField(blank=True, max_length=50, verbose_name='Название таблицы 3 гр 2 р')),
                ('description_1gr_1round', models.CharField(blank=True, max_length=50, verbose_name='Название таблицы 1 гр 1 р')),
                ('description_2gr_1round', models.CharField(blank=True, max_length=50, verbose_name='Название таблицы 2 гр 1 р')),
                ('description_3gr_1round', models.CharField(blank=True, max_length=50, verbose_name='Название таблицы 3 гр 1 р')),
                ('description_4gr_1round', models.CharField(blank=True, max_length=50, verbose_name='Название таблицы 4 гр 1 р')),
                ('season', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='description_table', to='rating.Season', verbose_name='Сезон')),
            ],
        ),
    ]
