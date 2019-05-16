from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from metcons.models import Classification, Movement, Workout, WorkoutInstance
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from metcons.forms import CreateWorkoutForm
import re


def index(request):
    """View function for home page of site"""
    num_workouts = Workout.objects.all().count()
    num_movements = Movement.objects.all().count()

    context = {
        'num_workouts': num_workouts,
        'num_movements': num_movements,
        }
    return render(request, 'index.html', context=context)

@login_required
def profile(request, username):
    users_workouts = WorkoutInstance.objects.filter(current_user=request.user).order_by('-date_added_by_user')

    context = {
        'users_workouts': users_workouts,
        }
    return render(request, 'metcons/user_page.html', context=context)
    
class WorkoutListView(generic.ListView):
    model = Workout
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super(WorkoutListView, self).get_context_data(**kwargs)
        context.update({
            'movement_list': Movement.objects.all(),
            'classification_list': Classification.objects.all(),
            'num_workouts_filtered': self.get_queryset().count(),
            'most_recent_workouts': Workout.objects.order_by('-date_created')[:10],
            'num_workouts_total': Workout.objects.all().count(),
        })
        return context

    def get_queryset(self):           
        object_list = Workout.objects.all()
        query1 = self.request.GET.getlist('q')
        query2 = self.request.GET.get('z')
        query3 = self.request.GET.get('x')
        query4 = self.request.GET.get('y')
        query5 = self.request.GET.get('t')
        
        if query1:
            for i in query1:
                if i != '':
                    object_list2 = object_list.filter(movements__name = i)
                    if not object_list2:
                        object_list2 = object_list.filter(movements__name = i.title())
                    object_list = object_list2
        if query2:
            if query2.islower():
                query2 = query2.title()
            object_list = object_list.filter(classification__name = query2)
        #could get rid of this ifand and just do if 3/if4 but I think the ifand will save
        # time by performing the queries at once rather than seperate
        if query3 and query4:
            object_list = object_list.filter(estimated_duration_in_minutes__gte=query3,
                                             estimated_duration_in_minutes__lte=query4)
        elif query3:
            object_list = object_list.filter(estimated_duration_in_minutes__gte=query3)
        elif query4:
            object_list = object_list.filter(estimated_duration_in_minutes__lte=query4,
                                             estimated_duration_in_minutes__gt=0)
        if query5:
            object_list = object_list.order_by('-number_of_times_completed')
        return object_list
    
def workoutdetailview(request, pk):
    workout = Workout.objects.get(id=pk)
    
    context = {
        'workout': workout,
        }

    if request.method == 'POST':
        workout = Workout.objects.get(id=str(request.POST['workout']))
        current_user = User.objects.get(username=str(request.POST['currentuser']))
        duration=0
        if re.findall(r'as possible in \d+ minutes of', workout.workout_text):
            r1=re.findall(r'as possible in \d+ minutes of', workout.workout_text)
            duration=int(re.split('\s', r1[0])[3])
        instance = WorkoutInstance(workout=workout, current_user = current_user,
                                   duration_in_minutes=duration)
        instance.save()

        return HttpResponseRedirect(instance.get_absolute_url())
    
    return render(request, 'metcons/workout_detail.html', context=context)
    
class WorkoutInstanceDetailView(LoginRequiredMixin, generic.DetailView):
    model = WorkoutInstance
    
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
            workout.update_movements_and_classification()

            current_user = User.objects.get(username=request.user.username)
            duration=0
            if re.findall(r'as possible in \d+ minutes of', workout.workout_text):
                r1=re.findall(r'as possible in \d+ minutes of', workout.workout_text)
                duration=int(re.split('\s', r1[0])[3])
                
            instance = WorkoutInstance(workout=workout, current_user=current_user,
                                       duration_in_minutes=duration)
            instance.save()
            
            return HttpResponseRedirect(instance.get_absolute_url())

    else:
        form = CreateWorkoutForm()

    context = {
        'form': form,
        }

    return render(request, 'metcons/create_workout.html', context)

class MovementCreate(CreateView):
    model = Movement
    fields = '__all__'
    
