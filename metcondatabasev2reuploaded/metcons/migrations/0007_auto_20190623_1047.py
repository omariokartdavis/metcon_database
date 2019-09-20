# Generated by Django 2.1.1 on 2019-06-23 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metcons', '0006_workoutinstance_datetime_to_unhide'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workoutinstance',
            name='datetime_to_unhide',
        ),
        migrations.AddField(
            model_name='workoutinstance',
            name='date_to_unhide',
            field=models.DateField(blank=True, null=True),
        ),
    ]
