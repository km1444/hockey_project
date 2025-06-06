# Generated by Django 3.2.23 on 2024-03-27 23:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0055_teamfortable_coach'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teamfortable',
            name='coach',
        ),
        migrations.AddField(
            model_name='teamfortable',
            name='coach_1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_for_tables_coach_1', to='rating.player', verbose_name='Тренер'),
        ),
        migrations.AddField(
            model_name='teamfortable',
            name='coach_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_for_tables_coach_2', to='rating.player', verbose_name='Тренер_2'),
        ),
        migrations.AddField(
            model_name='teamfortable',
            name='coach_3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_for_tables_coach_3', to='rating.player', verbose_name='Тренер_3'),
        ),
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
        migrations.AddField(
            model_name='teamfortable3',
            name='coach_1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_for_tables3_coach_1', to='rating.player', verbose_name='Тренер'),
        ),
        migrations.AddField(
            model_name='teamfortable3',
            name='coach_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_for_tables3_coach_2', to='rating.player', verbose_name='Тренер_2'),
        ),
        migrations.AddField(
            model_name='teamfortable3',
            name='coach_3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_for_tables3_coach_3', to='rating.player', verbose_name='Тренер_3'),
        ),
        migrations.AddField(
            model_name='teamfortable4',
            name='coach_1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_for_tables4_coach_1', to='rating.player', verbose_name='Тренер'),
        ),
        migrations.AddField(
            model_name='teamfortable4',
            name='coach_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_for_tables4_coach_2', to='rating.player', verbose_name='Тренер_2'),
        ),
        migrations.AddField(
            model_name='teamfortable4',
            name='coach_3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_for_tables4_coach_3', to='rating.player', verbose_name='Тренер_3'),
        ),
    ]
