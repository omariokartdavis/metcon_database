from metcons.models import Classification, Movement, Workout
import datetime as dt
import urllib.request
from bs4 import BeautifulSoup as bs
import re
from django.contrib.auth.models import User

user = User.objects.get(username='odavis')

#run with: exec(open('mainsite_workouts.py').read()) in python manage.py shell
#doesn't work for 2019 or <= 2017 as Crossfit Mainsite changed their format of posting workouts for those years
year = 2018
while year >= 2018:
    page_number = 1
    while page_number <= 12:
        mainsite_workouts = '{}{}{}{}'.format("https://www.crossfit.com/workout/",year,"?page=",page_number)
        page = urllib.request.urlopen(mainsite_workouts)
        soup = bs(page, "lxml")
    
        for eachworkout in soup.select('div[class="col-xs-12 col-sm-6 col-md-7 col-lg-7 content"]'):
            if eachworkout.find_all(string=re.compile(r'^Rest Day$')): #allows for exact match of the words. same below with Scaling
                continue
            for day in eachworkout.select('h3'):
                day_and_date = day.get_text()
                date = day_and_date[-6:]
                date_in_datetime = dt.datetime.strptime(date, "%y%m%d").date()
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
                    scaled = div.get_text()
                    continue
                w = []
                for paragraph in div.select('p'):
                    if paragraph.find_all(string=re.compile('Merry Christmas|Related|Scroll for scaling options|Compare|Post|Tips and Scaling')):
                        continue
                    workout_part = re.sub(r'(?<=[a-z])-(?=[a-z])', ' ', paragraph.get_text())
                    w.append(workout_part)
                workout_text = '\n'.join(w)
            workout = Workout(workout_text=workout_text,
                              scaling_or_description_text=scaling_text,
                              what_website_workout_came_from='Crossfit Mainsite',
                              classification=None,
                              date_created=date_in_datetime,
                              created_by_user=user,
                              )
            workout.save()
            workout.update_movements_and_classification()
        page_number += 1
    year -= 1
