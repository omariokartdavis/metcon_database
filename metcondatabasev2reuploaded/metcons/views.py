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
    
    def get_context_data(self, **kwargs):
        context = super(WorkoutListView, self).get_context_data(**kwargs)
        context.update({
            'movement_list': Movement.objects.all(),
        })
        return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            query = query.title()
            object_list = Workout.objects.filter(movements__name = query)
        else:
            object_list = Workout.objects.all()
        return object_list
    
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
                              classification=None,
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
    
