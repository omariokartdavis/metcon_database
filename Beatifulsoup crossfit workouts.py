import urllib.request
from bs4 import BeautifulSoup as bs
import re

year = 2018
while year >= 2017:
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
                print("\n",day_and_date,"\n")
            for div in eachworkout.select('div[class="col-sm-6"]'):
                if div.find_all(string=re.compile(r'^Scaling$|^Scaled Option$')):
                    scaling = div.get_text()
#                    print(scaling)
                    continue
                w = []
                for paragraph in div.select('p'):
                    if paragraph.find_all(string=re.compile('Merry Christmas|Related|Scroll for scaling options|Compare|Post|Tips and Scaling')):
                        continue
                    workout_part = paragraph.get_text()
                    w.append(workout_part)
                workout = '\n'.join(w)
                print(workout)
        page_number += 1
    year -= 1
