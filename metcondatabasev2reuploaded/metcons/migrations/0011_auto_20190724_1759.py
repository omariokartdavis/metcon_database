# Generated by Django 2.1.1 on 2019-07-24 22:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('metcons', '0010_auto_20190630_0927'),
    ]

    operations = [
        migrations.CreateModel(
            name='Set',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('set_number', models.IntegerField(default=1)),
                ('reps', models.IntegerField(blank=True, default=5, null=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True)),
                ('weight_units', models.CharField(blank=True, choices=[('lbs', 'lbs'), ('kgs', 'kgs'), ('%', '%')], default='lbs', max_length=1, null=True)),
            ],
            options={
                'ordering': ['set_number'],
            },
        ),
        migrations.CreateModel(
            name='StrengthExercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_added_to_database', models.DateTimeField(auto_now_add=True)),
                ('number_of_times_completed', models.IntegerField(default=0, verbose_name='Times Completed')),
                ('number_of_sets', models.IntegerField(blank=True, default=1, null=True, verbose_name='Sets')),
                ('movement', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='metcons.Movement')),
            ],
        ),
        migrations.CreateModel(
            name='StrengthWorkout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_added_to_database', models.DateTimeField(auto_now_add=True)),
                ('number_of_times_completed', models.IntegerField(default=0, verbose_name='Times Completed')),
                ('created_by_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('strength_exercises', models.ManyToManyField(blank=True, to='metcons.StrengthExercise')),
            ],
        ),
        migrations.AddField(
            model_name='workoutinstance',
            name='comment',
            field=models.TextField(blank=True, max_length=4000, null=True),
        ),
        migrations.AlterField(
            model_name='workoutinstance',
            name='workout',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='metcons.Workout'),
        ),
        migrations.AddField(
            model_name='set',
            name='strength_exercise',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='metcons.StrengthExercise'),
        ),
        migrations.AddField(
            model_name='workoutinstance',
            name='strength_workout',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='metcons.StrengthWorkout'),
        ),
    ]