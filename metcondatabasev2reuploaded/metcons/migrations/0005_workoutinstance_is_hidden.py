# Generated by Django 2.1.1 on 2019-06-23 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metcons', '0004_workoutinstance_assigned_by_coach_or_gym_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='workoutinstance',
            name='is_hidden',
            field=models.BooleanField(default=False),
        ),
    ]