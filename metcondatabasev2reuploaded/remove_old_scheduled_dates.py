#need to run this everyday
#python manage.py shell
#exec(open('remove_old_scheduled_dates.py').read())

from metcons.models import WorkoutInstance as wi

for i in wi.objects.all():
    i.remove_dates_to_be_completed_in_past()

