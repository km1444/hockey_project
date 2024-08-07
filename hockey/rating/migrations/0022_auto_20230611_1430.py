# Generated by Django 2.2.16 on 2023-06-11 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0021_auto_20230610_2233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playoff',
            name='team_1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='playoff_1', to='rating.Team', verbose_name='Команда_1'),
        ),
        migrations.AlterField(
            model_name='playoff',
            name='team_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='playoff_2', to='rating.Team', verbose_name='Команда_2'),
        ),
        migrations.AlterField(
            model_name='statistic',
            name='team',
            field=models.ForeignKey(blank=True, default=5, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='statistics', to='rating.Team', verbose_name='Команда'),
        ),
        migrations.AlterField(
            model_name='teamfortable2round',
            name='name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_for_tables_2_round', to='rating.TeamForTable', verbose_name='Команда'),
        ),
    ]
