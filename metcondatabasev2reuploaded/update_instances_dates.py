#python manage.py shell
#exec(open('name.py').read())

from metcons.models import WorkoutInstance as wi

instances = wi.objects.all()

for i in instances.iterator():
    i.update_youngest_scheduled_date()
    i.update_oldest_completed_date()
    i.save()
