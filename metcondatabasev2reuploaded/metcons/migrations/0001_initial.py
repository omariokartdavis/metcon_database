# Generated by Django 2.1.1 on 2019-04-18 20:48

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Classification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, choices=[('Upper Body', 'Upper Body'), ('Lower Body', 'Lower Body'), ('Total Body', 'Total Body'), ('Cardio', 'Cardio')], default='Total Body', help_text='Is this movement upper, lower, total body or cardio?', max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Movement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('classification', models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='metcons.Classification')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(default=datetime.date.today)),
                ('date_added_to_database', models.DateField(auto_now_add=True)),
                ('date_completed', models.DateField(auto_now=True)),
                ('number_of_times_completed', models.IntegerField(default=0)),
                ('workout_text', models.TextField(max_length=2000)),
                ('scaling_or_description_text', models.TextField(blank=True, max_length=4000, null=True)),
                ('what_website_workout_came_from', models.CharField(blank=True, max_length=200, null=True)),
                ('estimated_duration_in_minutes', models.IntegerField(blank=True, default=0, null=True)),
                ('classification', models.ForeignKey(blank=True, default=3, null=True, on_delete=django.db.models.deletion.CASCADE, to='metcons.Classification')),
                ('movements', models.ManyToManyField(blank=True, to='metcons.Movement')),
            ],
            options={
                'ordering': ['-number_of_times_completed', '-date_created', '-id'],
            },
        ),
    ]