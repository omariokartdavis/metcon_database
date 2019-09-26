from metcons.models import Workout, User
import datetime as dt
import urllib.request
from bs4 import BeautifulSoup as bs
import re
from django.utils import timezone

def get_todays_metcon():
    user = User.objects.get(username='odavis')
    
    year = dt.date.today().year
    page_number=1
    mainsite_workouts = '{}{}{}{}'.format("https://www.crossfit.com/workout/",year,"?page=",page_number)
    page = urllib.request.urlopen(mainsite_workouts)
    soup = bs(page, "lxml")
    
    
    for eachworkout in soup.select('div[class="col-xs-12 col-sm-6 col-md-7 col-lg-7 content"]'):
        if eachworkout.find_all(string=re.compile(r'^Rest Day$')): #allows for exact match of the words. same below with Scaling
            continue
        for day in eachworkout.select('h3'):
            day_and_date = day.get_text()
            date = day_and_date[-6:]
            date_in_datetime = timezone.make_aware(dt.datetime.strptime(date, "%y%m%d"))
        for div in eachworkout.select('div[class="col-sm-6"]'):
            if div.find_all(string=re.compile(r'^Scaling$')):
                scaling_text = div.get_text()
                scaling_text = scaling_text[10:]
                scaling_text = re.sub(r'(?<=[a-z])-(?=[a-z])', ' ', scaling_text)
            elif div.find_all(string=re.compile(r'^Scaled Option$')):
                scaling_text = div.get_text()
                scaling_text = scaling_text[16:]
                scaling_text = re.sub(r'(?<=[a-z])-(?=[a-z])', ' ', scaling_text)
            else:
                scaling_text = None
        for div in eachworkout.select('div[class="col-sm-6"]'):
            if div.find_all(string=re.compile(r'^Scaling$|^Scaled Option$')):
                continue
            if not div.get_text():
                continue #if there is no text then this will skip that div (in 2019 crossfit.com got rid of the scaling div text but left the div and just left it blank.)
                        # this allows me to skip that blank div without deleting the scaled text portion so that if they add it back in the future I will have it available.
            w = []
            for paragraph in div.select('p'):
                if paragraph.find_all(string=re.compile('Merry Christmas|Related|Scroll for scaling options|Compare|Post|Tips and Scaling')):
                    continue
                workout_part = re.sub(r'(?<=[a-z])-(?=[a-z])', ' ', paragraph.get_text())
                w.append(workout_part)
            workout_text = '\n'.join(w)
            if re.findall(r'as possible in \d+ minutes of', workout_text):
                r1=re.findall(r'as possible in \d+ minutes of', workout_text)
                duration=60*(int(re.split('\s', r1[0])[3]))           
            else:
                duration=0
        if not Workout.objects.filter(workout_text=workout_text).exists():
            workout = Workout(workout_text=workout_text,
                              scaling_or_description_text=scaling_text,
                              where_workout_came_from='Crossfit Mainsite',
                              classification=None,
                              date_created=date_in_datetime,
                              estimated_duration_in_seconds=duration,
                              created_by_user=user,
                              gender='B'
                              )
            workout.save()
            workout.update_movements_and_classification()
        break
