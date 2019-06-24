from metcons.models import WorkoutInstance as wi

for i in wi.objects.all().iterator():
    i.check_unhide_date()
