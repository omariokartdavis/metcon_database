from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(is_safe=True)
@stringfilter
def filter_workouts_based_on_movement(workout_list, movement_name):
    """Filters the list of available workouts based on the selected movement"""
    names_list = []
    filtered_list = []
    for i in workout_list:
        for a in i.movements:
            names_list.append(a.name)
        if movement_name in names_list:
            filtered_list.append(i)
    return filtered_list

#how do you get html to use this filter? if button is selected use filter
# otherwise return regular unfiltered list?
