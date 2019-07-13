from calendar import HTMLCalendar
from .models import WorkoutInstance
from django.db.models import Q
from django.utils import timezone
import datetime as dt

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None, this_user=None):
        self.year = year
        self.month = month
        self.this_user = this_user
        super(Calendar, self).__init__()

    # formats a day as a td
    # filter WorkoutInstance by day
    def formatday(self, day, instances):
        if day == 0:
            return '<td class="noday">&nbsp;</td>' #day outside month
        else:
            if int(day) < 10:
                day = "0" + str(day)
            date_string = str(self.year) + ", " + str(self.month) + ", " + str(day)
            date = timezone.make_aware(dt.datetime.strptime(date_string, "%Y, %m, %d")).date()
            instances_per_day = instances.filter(Q(dates_to_be_completed__date_completed=date) |
                                                 Q(dates_workout_completed__date_completed=date)).distinct()
            d = ''
            for instance in instances_per_day:
                    d += f'<li><a href="{ instance.get_absolute_url() }"> {instance.workout.display_name()} </a></li>'
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    # formats a week as a tr 
    def formatweek(self, theweek, instances):
        week = ''
        for d, weekday in theweek:
                week += self.formatday(d, instances)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter instances by year and month
    def formatmonth(self, withyear=True):
        instances = WorkoutInstance.objects.filter(Q(current_user=self.this_user, dates_to_be_completed__date_completed__year=self.year, dates_to_be_completed__date_completed__month=self.month) |
                                                   Q(current_user=self.this_user, dates_workout_completed__date_completed__year=self.year, dates_workout_completed__date_completed__month=self.month)).distinct()

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
                cal += f'{self.formatweek(week, instances)}\n'
        return cal
