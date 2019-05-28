#python manage.py shell
#exec(open('name.py').read())

from metcons.models import WorkoutInstance as wi

instances = wi.objects.all()

for i in instances.iterator():
    i.update_edited_workout_text()
    i.update_edited_scaling_text()
    i.save()
