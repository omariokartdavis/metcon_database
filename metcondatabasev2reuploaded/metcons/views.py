from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from metcons.models import Classification, Movement, Workout, WorkoutInstance, Result, ResultFile, Date
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from metcons.forms import CreateWorkoutForm, CreateResultForm, ScheduleInstanceForm, EditInstanceForm, EditResultForm
from django.utils import timezone
import datetime as dt
from django.db.models import Max, Min, Q
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
    #if there isn't a completed date it is last then filtered by date_added_by_user
    users_workouts = WorkoutInstance.objects.filter(current_user=request.user)

    now = timezone.localtime(timezone.now()).date()
    future_workouts = WorkoutInstance.objects.filter(current_user=request.user,
                                                     dates_to_be_completed__date_completed__gte=now).exclude(
                                                         youngest_scheduled_date__date_completed=now,
                                                         dates_workout_completed__date_completed=now).exclude(
                                                             youngest_scheduled_date=None).distinct().order_by('-youngest_scheduled_date')

    recent_time = now - timezone.timedelta(days=14)
    recent_past_workouts = WorkoutInstance.objects.filter(current_user=request.user,
                                                          dates_workout_completed__date_completed__lte=now,
                                                          dates_workout_completed__date_completed__gte=recent_time).distinct().order_by('oldest_completed_date', '-youngest_scheduled_date')
    
    long_past_workouts = WorkoutInstance.objects.filter(current_user=request.user,
                                                        dates_workout_completed__date_completed__lt=recent_time).exclude(
                                                            dates_workout_completed__date_completed__gte=recent_time).distinct().order_by('oldest_completed_date')
    other_workouts = WorkoutInstance.objects.filter(current_user=request.user,
                                                    dates_to_be_completed=None,
                                                    dates_workout_completed=None).distinct().order_by('date_added_by_user')

    context = {
        'users_workouts': users_workouts,
        'future_workouts': future_workouts,
        'recent_past_workouts': recent_past_workouts,
        'long_past_workouts': long_past_workouts,
        'other_workouts': other_workouts,
        }
    return render(request, 'metcons/user_page.html', context=context)

@login_required
def profileredirect(request):
    return HttpResponseRedirect(reverse('profile', args=[request.user.username]))

def workoutlistview(request):
    # default object list excludes users workouts that have been completed.
    object_list = Workout.objects.all()
    
    query1 = request.GET.getlist('q')
    query2 = request.GET.get('z')
    query3 = request.GET.get('x')
    query4 = request.GET.get('y')
    query5 = request.GET.get('t')
    query6 = request.GET.get('s')
    query7 = request.GET.get('f')
    
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
    if query3:
        object_list = object_list.filter(estimated_duration_in_seconds__gte=query3)
    if query4:
        object_list = object_list.filter(estimated_duration_in_seconds__lte=query4,
                                         estimated_duration_in_seconds__gt=0)
    if query5:
        object_list = object_list.order_by('-number_of_times_completed')
    if not query6:
        object_list = object_list.exclude(workoutinstance__current_user=request.user,
                                          workoutinstance__dates_workout_completed__isnull=False)
    if not query7:
        object_list = object_list.exclude(~Q(created_by_user=request.user),
                                          where_workout_came_from='User Created')
        
        

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
                instance.update_edited_workout_text()
                instance.update_edited_scaling_text()
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
                instance.update_edited_workout_text()
                instance.update_edited_scaling_text()
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
        result_list = Result.objects.filter(workoutinstance = instance).order_by('-date_workout_completed', '-date_created')
        context['result_list'] = result_list
            
        return context
    
class MovementListView(generic.ListView):
    model = Movement
    paginate_by = 10

class MovementDetailView(generic.DetailView):
    model = Movement

@login_required
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
                
                if form.cleaned_data['repeat_yes'] == True:
                    repeat_frequency = form.cleaned_data['repeat_frequency']
                    number_of_repetitions = form.cleaned_data['number_of_repetitions']
                    repeat_length = form.cleaned_data['repeat_length']
                    end_repeat_scheduling_date = local_date + timezone.timedelta(repeat_length=number_of_repetitions)
                    list_of_dates_to_schedule = [local_date]
                    while local_date < end_repeat_scheduling_date:
                        list_of_dates_to_schedule.append(local_date + timezone.timedelta(repeat_frequency=1))
                        local_date += timezone.timedelta(repeat_frequency=1)
                        
                print(local_date)
                print(list_of_dates_to_schedule)
                #instance.add_date_to_be_completed(local_date)
                
                return HttpResponseRedirect(reverse('profile', args=[request.user.username]))
    else:
        form = ScheduleInstanceForm()

    context = {
        'form': form,
        'instance': instance,
        }

    return render(request, 'metcons/schedule_instance.html', context)

@login_required
def edit_instance(request, username, pk):
    instance = WorkoutInstance.objects.get(id=pk)

    if request.method == 'POST':
        if 'edit instance' in request.POST:
            form = EditInstanceForm(request.POST)
            if form.is_valid():
                base_workout = instance.workout
                instance.edited_workout_text = form.cleaned_data['workout_text']
                instance.edited_scaling_text = form.cleaned_data['scaling_text']
                instance.duration_in_seconds = ((form.cleaned_data['duration_minutes'])*60) + form.cleaned_data['duration_seconds']
                instance.save()
                if base_workout:
                    if request.user == base_workout.created_by_user:
                        if base_workout.number_of_instances() == 1:
                            base_workout.workout_text = form.cleaned_data['workout_text']
                            base_workout.scaling_or_description_text = form.cleaned_data['scaling_text']
                            base_workout.estimated_duration_in_seconds = ((form.cleaned_data['duration_minutes'])*60) + form.cleaned_data['duration_seconds']
                            base_workout.save()
                            base_workout.update_movements_and_classification()
                        base_workout.update_estimated_duration()


                return HttpResponseRedirect(instance.get_absolute_url())
    else:
        if instance.duration_in_seconds:
            duration_minutes=instance.duration_in_seconds // 60
            duration_seconds=instance.duration_in_seconds % 60
        else:
            duration_minutes=0
            duration_seconds=0
        form = EditInstanceForm(initial={'duration_minutes': duration_minutes,
                                         'duration_seconds': duration_seconds,
                                         'workout_text': instance.edited_workout_text,
                                         'scaling_text': instance.edited_scaling_text,
                                         })

    context = {
        'form': form,
        'instance': instance,
        }

    return render(request, 'metcons/edit_instance.html', context)

@login_required
def delete_instance(request, username, pk):
    instance = WorkoutInstance.objects.get(id=pk)

    if request.method == 'POST':
        if request.user == instance.current_user:
            base_workout = instance.workout
            instance.delete()
            base_workout.update_estimated_duration()
            base_workout.update_times_completed()

            return HttpResponseRedirect(reverse('profile', args=[username]))

    context = {
        'instance': instance,
        }

    return render(request, 'metcons/delete_instance.html', context)

@login_required                
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
                instance.add_date_completed(timezone.localtime(result.date_workout_completed).date())
                result.update_instance_duration()
                instance.update_times_completed()
                
                if request.FILES:
                    resultfile = ResultFile(result=result,
                                        caption = form.cleaned_data['media_file_caption'],
                                        file=request.FILES['media_file'],
                                        content_type = request.FILES['media_file'].content_type)
                    resultfile.save()                                            

                return HttpResponseRedirect(instance.get_absolute_url())
    else:
        if instance.duration_in_seconds:
            duration_minutes=instance.duration_in_seconds // 60
            duration_seconds=instance.duration_in_seconds % 60
        else:
            duration_minutes=0
            duration_seconds=0
        form = CreateResultForm(initial={'duration_minutes': duration_minutes, 'duration_seconds': duration_seconds})

    context = {
        'form': form,
        'instance': instance,
        }

    return render(request, 'metcons/create_result.html', context)

@login_required
def edit_result(request, username, pk, resultid):
    #currently not handling edits of resultfiles. add request.FILES into form if going to do so
    result = Result.objects.get(id=resultid)
    instance = WorkoutInstance.objects.get(id=pk)
    
    if request.method == 'POST':
        if 'edit result' in request.POST:
            form = EditResultForm(request.POST)

            if form.is_valid():
                duration_in_seconds = ((form.cleaned_data['duration_minutes']) * 60) + form.cleaned_data['duration_seconds']
                if form.cleaned_data['date_completed'] == dt.date.today():
                    aware_datetime = timezone.now()
                else:
                    date_in_datetime = dt.datetime.combine(form.cleaned_data['date_completed'], dt.datetime.min.time())
                    aware_datetime=timezone.make_aware(date_in_datetime)
                if result.duration_in_seconds != duration_in_seconds:
                    result.duration_in_seconds = duration_in_seconds
                if result.result_text != form.cleaned_data['result_text']:
                    result.result_text = form.cleaned_data['result_text']
                local_aware_datetime = timezone.localtime(aware_datetime)
                if timezone.localtime(result.date_workout_completed).date() != local_aware_datetime.date():
                    instance.remove_date_completed(timezone.localtime(result.date_workout_completed).date())
                    result.date_workout_completed = aware_datetime
                result.save()
                instance.add_date_completed(timezone.localtime(result.date_workout_completed).date())
                result.update_instance_duration()

                return HttpResponseRedirect(instance.get_absolute_url())
    else:
        if result.duration_in_seconds:
            duration_minutes=result.duration_in_seconds // 60
            duration_seconds=result.duration_in_seconds % 60
        else:
            duration_minutes=0
            duration_seconds=0
        form = EditResultForm(initial={'duration_minutes': duration_minutes,
                                        'duration_seconds': duration_seconds,
                                        'result_text': result.result_text,
                                        'date_completed': result.date_workout_completed,
                                        })
    context = {
        'form': form,
        'instance': instance,
        'result': result,
        }

    return render(request, 'metcons/edit_result.html', context)

@login_required
def delete_result(request, username, pk, resultid):
    instance = WorkoutInstance.objects.get(id=pk)
    result = Result.objects.get(id=resultid)
    
    if request.method == 'POST':
        if 'delete result' in request.POST:
            if request.user == instance.current_user:
                instance.remove_date_completed(timezone.localtime(result.date_workout_completed).date())
                result.delete()
                instance.update_duration()
                instance.update_times_completed()

                return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        'instance': instance,
        'result': result,
        }

    return render(request, 'metcons/delete_result.html', context)

@login_required    
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
                                  where_workout_came_from='User Created',
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
                instance.update_edited_workout_text()
                instance.update_edited_scaling_text()
                instance.save()
            else:
                workout = Workout.objects.get(workout_text=form.cleaned_data['workout_text'])
                if not WorkoutInstance.objects.filter(workout=workout, current_user=current_user):
                    instance = WorkoutInstance(workout=workout, current_user = current_user,
                                               duration_in_seconds=workout.estimated_duration_in_seconds)
                    instance.save()
                    instance.update_edited_workout_text()
                    instance.update_edited_scaling_text()
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

class MovementCreate(LoginRequiredMixin, CreateView):
    model = Movement
    fields = '__all__'

