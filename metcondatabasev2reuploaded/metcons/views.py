from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from metcons.models import Classification, Movement, Workout, WorkoutInstance, Result, ResultFile
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from metcons.forms import CreateWorkoutForm, CreateResultForm, ScheduleInstanceForm
from django.utils import timezone
import datetime as dt
from django.db.models import Max, Min
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
    #new order function orders by latest completed date on workout instance
    #if there isn't a completed date it is last then filtered by date_added_by_user
    # might need the opposite of this for future scheduled workouts
    users_workouts = WorkoutInstance.objects.annotate(max_date=Max('dates_workout_completed__date_completed')).filter(current_user=request.user).order_by('-max_date', '-date_added_by_user')
    now = timezone.now()
    future_workouts = WorkoutInstance.objects.annotate(min_date=Min('dates_to_be_completed__date_completed')).filter(current_user=request.user,
                                                                                                                     dates_to_be_completed__date_completed__gte=now).distinct().order_by('min_date')
    recent_time = now - timezone.timedelta(days=14)
    recent_past_workouts = WorkoutInstance.objects.annotate(max_date=Max('dates_workout_completed__date_completed')).filter(current_user=request.user,
                                                                                                                            dates_workout_completed__date_completed__lt=now,
                                                                                                                            dates_workout_completed__date_completed__gte=recent_time).distinct().order_by('-max_date')
    long_past_workouts = WorkoutInstance.objects.annotate(max_date=Max('dates_workout_completed__date_completed')).filter(current_user=request.user,
                                                                                                                          dates_workout_completed__date_completed__lt=recent_time).distinct().order_by('-max_date')
    #old order function:
    #WorkoutInstance.objects.filter(current_user=request.user).order_by('-date_added_by_user')
    context = {
        'users_workouts': users_workouts,
        'future_workouts': future_workouts,
        'recent_past_workouts': recent_past_workouts,
        'long_past_workouts': long_past_workouts,
        }
    return render(request, 'metcons/user_page.html', context=context)

@login_required
def profileredirect(request):
    return HttpResponseRedirect(reverse('profile', args=[request.user.username]))

def workoutlistview(request):

    object_list = Workout.objects.all()
    query1 = request.GET.getlist('q')
    query2 = request.GET.get('z')
    query3 = request.GET.get('x')
    query4 = request.GET.get('y')
    query5 = request.GET.get('t')
    if query3:
        query3 = int(query3) * 60
    if query4:
        query4 = int(query4) * 60
        
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
        #likely have to change query3 and 4 to be *60
        object_list = object_list.filter(estimated_duration_in_seconds__gte=query3,
                                         estimated_duration_in_seconds__lte=query4)
    elif query3:
        object_list = object_list.filter(estimated_duration_in_seconds__gte=query3)
    elif query4:
        object_list = object_list.filter(estimated_duration_in_seconds__lte=query4,
                                         estimated_duration_in_seconds__gt=0)
    if query5:
        object_list = object_list.order_by('-number_of_times_completed')
        

    context = {
        'workout_list': object_list,
        'num_workouts_filtered': object_list.count(),
        'movement_list': Movement.objects.all(),
        'classification_list': Classification.objects.all(),
        'most_recent_workouts': Workout.objects.order_by('-date_created')[:10],
        'num_workouts_total': Workout.objects.all().count(),
        }

    if request.method == 'POST':
        if 'add_workout_to_profile' in request.POST:
            workout = Workout.objects.get(id=str(request.POST['workout']))
            current_user = User.objects.get(username=str(request.POST['currentuser']))
            if not WorkoutInstance.objects.filter(workout=workout, current_user=current_user):
                instance = WorkoutInstance(workout=workout, current_user = current_user,
                                           duration_in_seconds=workout.estimated_duration_in_seconds)
                instance.save()
            else:
                instance = WorkoutInstance.objects.get(workout=workout, current_user=current_user)
            return HttpResponseRedirect(instance.get_absolute_url())
        
    return render(request, 'metcons/workout_list.html', context = context)
    
def workoutdetailview(request, pk):
    workout = Workout.objects.get(id=pk)
    duration_in_seconds = workout.estimated_duration_in_seconds
    if duration_in_seconds:
        duration_in_minutes = (duration_in_seconds // 60)
    else:
        duration_in_minutes = 0
    context = {
        'workout': workout,
        'estimated_duration': duration_in_minutes,
        }

    if request.method == 'POST':
        if 'add_workout_to_profile' in request.POST:
            workout = Workout.objects.get(id=str(request.POST['workout']))
            current_user = User.objects.get(username=str(request.POST['currentuser']))
            if not WorkoutInstance.objects.filter(workout=workout, current_user=current_user):
                instance = WorkoutInstance(workout=workout, current_user = current_user,
                                           duration_in_seconds=workout.estimated_duration_in_seconds)
                instance.save()
            else:
                instance = WorkoutInstance.objects.get(workout=workout, current_user=current_user)
            return HttpResponseRedirect(instance.get_absolute_url())
    
    return render(request, 'metcons/workout_detail.html', context=context)
    
class WorkoutInstanceDetailView(LoginRequiredMixin, generic.DetailView):
    model = WorkoutInstance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.get_object()
        duration_in_seconds = instance.duration_in_seconds
        if duration_in_seconds:
            duration_minutes = (duration_in_seconds // 60)
            duration_seconds = duration_in_seconds % 60
        else:
            duration_minutes = 0
            duration_seconds = 0
        context['duration_minutes'] = duration_minutes
        context['duration_seconds'] = duration_seconds
        result_list = Result.objects.filter(workoutinstance = instance).order_by('-date_created')
        context['result_list'] = result_list
            
        return context
    
class MovementListView(generic.ListView):
    model = Movement
    paginate_by = 10

class MovementDetailView(generic.DetailView):
    model = Movement

def schedule_instance(request, username, pk):
    instance = WorkoutInstance.objects.get(id=pk)
    if request.method == 'POST':
        if 'schedule instance' in request.POST:
            form = ScheduleInstanceForm(request.POST)
            if form.is_valid():
                if form.cleaned_data['date_to_be_completed1'] == dt.date.today():
                    aware_datetime = timezone.now()
                else:
                    date_in_datetime = dt.datetime.combine(form.cleaned_data['date_to_be_completed1'], dt.datetime.min.time())
                    aware_datetime = timezone.make_aware(date_in_datetime)

                local_date = timezone.localtime(aware_datetime).date()
                instance.add_date_to_be_completed(local_date)
                
                return HttpResponseRedirect(reverse('profile', args=[request.user.username]))
    else:
        form = ScheduleInstanceForm()

    context = {
        'form': form,
        'instance': instance,
        }

    return render(request, 'metcons/schedule_instance.html', context)
                
def create_result(request, username, pk):
    instance = WorkoutInstance.objects.get(id=pk)
    if request.method == 'POST':
        if 'add result to instance' in request.POST:
            form = CreateResultForm(request.POST, request.FILES)

            if form.is_valid():
                duration_in_seconds = ((form.cleaned_data['duration_minutes']) * 60) + form.cleaned_data['duration_seconds']
                if form.cleaned_data['date_completed'] == dt.date.today():
                    aware_datetime = timezone.now()
                else:
                    date_in_datetime = dt.datetime.combine(form.cleaned_data['date_completed'], dt.datetime.min.time())
                    aware_datetime=timezone.make_aware(date_in_datetime)
                result = Result(workoutinstance=instance,
                                result_text=form.cleaned_data['result_text'],
                                duration_in_seconds=duration_in_seconds,
                                date_workout_completed=aware_datetime)
                result.save()
                if request.FILES:
                    resultfile = ResultFile(result=result,
                                        caption = form.cleaned_data['media_file_caption'],
                                        file=request.FILES['media_file'],
                                        content_type = request.FILES['media_file'].content_type)
                    resultfile.save()                                            

                return HttpResponseRedirect(instance.get_absolute_url())
    else:
        form = CreateResultForm()

    context = {
        'form': form,
        'instance': instance,
        }

    return render(request, 'metcons/create_result.html', context)
                                
    
def create_workout(request):
    """View function for creating a new workout"""

    if request.method == 'POST':
        form = CreateWorkoutForm(request.POST)

        if form.is_valid():
            current_user = User.objects.get(username=request.user.username)
            if not Workout.objects.filter(workout_text=form.cleaned_data['workout_text']):
                workout = Workout(workout_text=form.cleaned_data['workout_text'],
                                  scaling_or_description_text=form.cleaned_data['workout_scaling'],
                                  estimated_duration_in_seconds=(form.cleaned_data['estimated_duration']) * 60,
                                  what_website_workout_came_from=form.cleaned_data['what_website_workout_came_from'],
                                  classification=None,
                                  created_by_user = current_user,
                                  )
                workout.save()
                if Workout.objects.filter(id=workout.id, workout_text__iregex=r'as possible in \d+ minutes of'):
                    r1=re.findall(r'as possible in \d+ minutes of', workout.workout_text)
                    workout.estimated_duration_in_seconds=int(re.split('\s', r1[0])[3])
                workout.update_movements_and_classification()
                    
                instance = WorkoutInstance(workout=workout, current_user=current_user,
                                           duration_in_seconds=workout.estimated_duration_in_seconds)
                instance.save()
            else:
                workout = Workout.objects.get(workout_text=form.cleaned_data['workout_text'])
                if not WorkoutInstance.objects.filter(workout=workout, current_user=current_user):
                    instance = WorkoutInstance(workout=workout, current_user = current_user,
                                               duration_in_seconds=workout.estimated_duration_in_seconds)
                    instance.save()
                else:
                    instance = WorkoutInstance.objects.get(workout=workout, current_user=current_user)
            
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
    
