class MovementList:
    movement_list = {
        'Pull Up': 'Upper Body',
        'Chest To Bar': 'Upper Body',
        'CTB': 'Upper Body',
        'Push Up': 'Upper Body',
        'Overhead Press': 'Upper Body',
        'Incline Bench': 'Upper Body',
        'Bench': 'Upper Body',
        'Handstand Push Up': 'Upper Body',
        'Jerk': 'Upper Body',
        'Split Jerk': 'Upper Body',
        'Run': 'Cardio',
        'Bike': 'Cardio',
        'Swim': 'Cardio',
        'Row': 'Cardio',
        'Ski Erg': 'Cardio',
        'Squat': 'Lower Body',
        'Front Squat': 'Lower Body',
        'Back Squat': 'Lower Body',
        'Overhead Squat': 'Total Body',
        'Thruster': 'Total Body',
        'Wall Ball': 'Total Body',
        'Burpee': 'Total Body',
        'Snatch': 'Total Body',
        'Overhead Squat': 'Total Body',
        'Burpee Over Bar': 'Total Body',
        'Bar Facing Burpee': 'Total Body',
        }

# to call this function to add movements to the database run:
# python manage.py runserver
# exec(open('metcons\movements_list.py').read())

from metcons.models import Classification, Movement, Workout

all_movements = MovementList()
current_movements_in_database = Movement.objects.all()
current_movements_in_database_names = [i.name for i in current_movements_in_database]    

for k, v in all_movements.movement_list.items():
    if k not in current_movements_in_database_names:
        movement = Movement(name=k, classification=Classification.objects.get(name=v))
        movement.save()

    
##to change this to include abbreviations later:
##change movement_list to a list of lists:
##movement_list = [
##  ['Pull Up', 'Upper Body', ['abbrvs']],...]
##
##then in the for loop just use:
##for i in all_movements:
##  for x, y, z in i:
##      movement = Movement( name=x,
##                  classification=Classification.objects.get(name=y),
##                  abbreviations= [a for a in z]
