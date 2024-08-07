# Generated by Django 3.2.23 on 2024-02-28 00:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0050_auto_20240225_0044'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamfortable2',
            name='coach_1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_for_tables2_coach_1', to='rating.player', verbose_name='Тренер'),
        ),
        migrations.AddField(
            model_name='teamfortable2',
            name='coach_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_for_tables2_coach_2', to='rating.player', verbose_name='Тренер_2'),
        ),
        migrations.AddField(
            model_name='teamfortable2',
            name='coach_3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_for_tables2_coach_3', to='rating.player', verbose_name='Тренер_3'),
        ),
    ]
