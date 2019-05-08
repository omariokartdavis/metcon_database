from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from metcons.models import Classification, Movement, Workout
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView

from metcons.forms import CreateWorkoutForm

def index(request):
    """View function for home page of site"""
    num_workouts = Workout.objects.all().count()
    num_movements = Movement.objects.all().count()

    context = {
        'num_workouts': num_workouts,
        'num_movements': num_movements,
        }
    return render(request, 'index.html', context=context)

class WorkoutListView(generic.ListView):
    model = Workout
    paginate_by = 10

class WorkoutDetailView(generic.DetailView):
    model = Workout

class MovementListView(generic.ListView):
    model = Movement
    paginate_by = 10

class MovementDetailView(generic.DetailView):
    model = Movement

def create_workout(request):
    """View function for creating a new workout"""

    if request.method == 'POST':
        form = CreateWorkoutForm(request.POST)

        if form.is_valid():
            workout = Workout(workout_text=form.cleaned_data['workout_text'],
                              scaling_or_description_text=form.cleaned_data['workout_scaling'],
                              estimated_duration_in_minutes=form.cleaned_data['estimated_duration'],
                              what_website_workout_came_from=form.cleaned_data['what_website_workout_came_from'],
                              classifications=None,
                              )
            workout.save()
            #can't update movements and class until the workout has a valid id
            workout.update_movements()
            workout.update_classification()
            workout.save()
            
            return HttpResponseRedirect(workout.get_absolute_url())

    else:
        form = CreateWorkoutForm()

    context = {
        'form': form,
        }

    return render(request, 'metcons/create_workout.html', context)

class MovementCreate(CreateView):
    model = Movement
    fields = '__all__'
    
##class WorkoutCreate(CreateView):
##    model = Workout
##    fields = ['workout_text',
##              'scaling_or_description_text',
##              'what_website_workout_came_from',
##              'estimated_duration_in_minutes',
##              'classifications',
##              ]
##    #exclude = ['classifications']
##    #model.classifications = None
##    initial = {'classifications': Classification.objects.get(name='Total Body')}
              
