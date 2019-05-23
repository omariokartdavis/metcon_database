#run this when you have added a new movement/classification to the database
# and want to update all current workouts in database with new tags

#to run this:
#python manage.py shell
#exec(open('update_all_workout_movement_and_class_tags.py').read())

from metcons.models import Classification, Movement, Workout

all_workouts = Workout.objects.all()

for i in all_workouts.iterator():
    i.update_movements_and_classification()
