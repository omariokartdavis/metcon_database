#imports all movements and classifications listed below as well as adds the past year of dates
# to possible workout instance completed dates


class MovementList:
    u = 'Upper Body'
    t = 'Total Body'
    l = 'Lower Body'
    c = 'Cardio'
    co = 'Core'

    movement_list = {
        'Pull Up': u,
        'Chest To Bar Pull Up': u,
        'Chin Over Bar Pull Up': u,
        'Dip': u,
        'Ring Dip': u,
        'Strict Ring Dip': u,
        'Ring Handstand Push Up': u,
        'Push Up': u,
        'Overhead Press': u,
        'Push Press': u,
        'Shoulder To Overhead': u,
        'Incline Bench': u,
        'Bench': u,
        'Handstand Push Up': u,
        'Handstand Walk': u,
        'Jerk': u,
        'Split Jerk': u,
        'Muscle Up': u,
        'Ring Muscle Up': u,
        'Bar Muscle Up': u,
        'Strict Muscle Up': u,
        'Strict Bar Muscle Up': u,
        'Strict Ring Muscle Up': u,
        'Strict Pull Up': u,
        'Kipping Pull Up': u,
        'Dumbbell Bench': u,
        'Push Jerk': u,
        'Dumbbell Push Jerk': u,
        'Double Under': u,
        'Toes To Bar': u,
        'Rope Climb': u,
        'Legless Rope Climb': u,
        'Run': c,
        'Bike': c,
        'Swim': c,
        'Row': c,
        'Ski Erg': c,
        'Sprint': c,
        'Any': c,
        'Squat': l,
        'Front Squat': l,
        'Back Squat': l,
        'Clean': l,
        'Deadlift': l,
        'Air Squat': l,
        'Box Jump': l,
        'Step Up': l,
        'Power Clean': l,
        'Hang Power Clean': l,
        'Hang Clean': l,
        'High Hang Clean': l,
        'Medicine Ball Clean': l,
        'Squat Clean': l,
        'Pistol': l,
        'Sumo Deadlift': l,
        'Lunge': l,
        'Glue Ham Raise': l,
        'Overhead Squat': t,
        'Thruster': t,
        'Wall Ball': t,
        'Burpee': t,
        'Burpee Over The Bar': t,
        'Bar Facing Burpee': t,
        'Snatch': t,
        'Squat Snatch': t,
        'Overhead Squat': t,
        'Burpee Over Bar': t,
        'Bar Facing Burpee': t,
        'Clean and Jerk': t,
        'Kettlebell Swing': t,
        'Power Snatch': t,
        'Sumo Deadlift High Pull': t,
        'Hang Dumbbell Snatch': t,
        'Dumbbell Power Snatch': t,
        'Dumbbell Snatch': t,
        'Overhead Walking Lunge': t,
        'Turkish Get Up': t,
        'Sit Up': co,
        'GHD Sit Up': co,
        'L Sit': co,
        'V Up': co,
        'Plank': co,
        }

class ClassificationList:
    class_list = ['Upper Body', 'Lower Body', 'Total Body', 'Cardio', 'Core']

# to call this function to add movements to the database run:
# python manage.py shell
# exec(open('movements_list.py').read())

from metcons.models import *
from django.utils import timezone
#import datetime as dt

##all_wicd = Date.objects.all()
##wicd_dates = []
##for i in all_wicd:
##    wicd_dates.append(i.date_completed)

num_users_per_category = 5

for i in range(1, num_users_per_category+1):
    if not User.objects.filter(username=f'testathlete{i}').exists():
        User.objects.create_user(username=f'testathlete{i}', password='4a0308ki9ps', is_athlete=True)
    if not User.objects.filter(username=f'testcoach{i}').exists():
        User.objects.create_user(username=f'testcoach{i}', password='4a0308ki9ps', is_coach=True)
    if not User.objects.filter(username=f'testgymowner{i}').exists():
        User.objects.create_user(username=f'testgymowner{i}', password='4a0308ki9ps', is_gym_owner=True)
    testathlete_user = User.objects.get(username=f'testathlete{i}')
    testcoach_user = User.objects.get(username=f'testcoach{i}')
    testgymowner_user = User.objects.get(username=f'testgymowner{i}')
    if not Athlete.objects.filter(user=testathlete_user).exists():
        Athlete.objects.create(user=testathlete_user)
    if not Athlete.objects.filter(user=testcoach_user).exists():
        Athlete.objects.create(user=testcoach_user)
    if not Athlete.objects.filter(user=testgymowner_user).exists():
        Athlete.objects.create(user=testgymowner_user)
    if not Coach.objects.filter(user=testcoach_user).exists():
        Coach.objects.create(user=testcoach_user)
    if not Coach.objects.filter(user=testgymowner_user).exists():
        Coach.objects.create(user=testgymowner_user)
    if not GymOwner.objects.filter(user=testgymowner_user).exists():
        GymOwner.objects.create(user=testgymowner_user)
    
for i in range(366):
    date = timezone.localtime(timezone.now()).date() - timezone.timedelta(days=i)
    if not Date.objects.filter(date_completed=date).exists():
        Date.objects.create(date_completed=date)

for i in range(1, 366):
    date = timezone.localtime(timezone.now()).date() + timezone.timedelta(days=i)
    if not Date.objects.filter(date_completed=date).exists():
        Date.objects.create(date_completed=date)

all_classifications = ClassificationList()
current_classifications_in_database = Classification.objects.all()
current_classifications_in_database_names = [i.name for i in current_classifications_in_database]

for k in all_classifications.class_list:
    if k not in current_classifications_in_database_names:
        Classification.objects.create(name=k)

all_movements = MovementList()
current_movements_in_database = Movement.objects.all()
current_movements_in_database_names = [i.name for i in current_movements_in_database]    

for k, v in all_movements.movement_list.items():
    if k not in current_movements_in_database_names:
        Movement.objects.create(name=k, classification=Classification.objects.get(name=v))

if not StrengthProgram.objects.filter(name='nSuns 531 LP').exists():
    StrengthProgram.objects.create(name='nSuns 531 LP', weight_increase_timeline='weekly')

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
