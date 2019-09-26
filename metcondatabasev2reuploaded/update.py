from apscheduler.schedulers.background import BackgroundScheduler
import mainsite_most_recent_workout
import datetime as dt

    
time_to_start = dt.datetime.combine(dt.date.today(), dt.time(20, 53)) #sometime before 8:30 pm crossfit.com puts up the metcon for the next day
#time_to_stop = dt.datetime.combine(dt.date.today(), dt.time(15,0))

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(mainsite_most_recent_workout.get_todays_metcon, 'interval', hours=24, start_date = time_to_start, id='get_todays_metcon')
    scheduler.start()

#try:
#    start()
#except (KeyboardInterrupt, SystemExit):
#    pass