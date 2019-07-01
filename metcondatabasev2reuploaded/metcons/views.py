from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from metcons.models import *
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from metcons.forms import *
from django.utils import timezone
import datetime as dt
from django.db.models import Max, Min, Q
from django.core.paginator import Paginator
import re
from django.contrib.auth import login, authenticate

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
    #long future workouts is 1 week forward, long past workouts is 2 weeks back
    users_workouts = WorkoutInstance.objects.filter(current_user=request.user)
    request_list = Request.objects.filter(requestee=request.user)

    now = timezone.localtime(timezone.now()).date()
    end_of_week = now + timezone.timedelta(days=7)
    long_future_workouts = WorkoutInstance.objects.filter(current_user=request.user,
                                                          youngest_scheduled_date__date_completed__gte=end_of_week).exclude(
                                                                  youngest_scheduled_date=None).distinct().order_by('-youngest_scheduled_date')


    recent_time = now - timezone.timedelta(days=14)
    recent_past_workouts = WorkoutInstance.objects.filter(current_user=request.user,
                                                          dates_workout_completed__date_completed__lte=now,
                                                          dates_workout_completed__date_completed__gte=recent_time).distinct().order_by('oldest_completed_date', '-youngest_scheduled_date')
    
    long_past_workouts = WorkoutInstance.objects.filter(current_user=request.user,
                                                        dates_workout_completed__date_completed__lt=recent_time).exclude(
                                                            dates_workout_completed__date_completed__gte=recent_time).distinct().order_by('oldest_completed_date')
    other_workouts = WorkoutInstance.objects.filter(current_user=request.user,
                                                    youngest_scheduled_date=None,
                                                    dates_workout_completed=None).distinct().order_by('date_added_by_user')

    dict_of_this_weeks_workouts = {}
    todays_workouts = WorkoutInstance.objects.filter(current_user=request.user,
                                           dates_to_be_completed__date_completed=now).exclude(
                                               dates_workout_completed__date_completed=now).exclude(
                                                   youngest_scheduled_date=None).distinct().order_by('-youngest_scheduled_date', 'date_added_by_user')
    if todays_workouts:
        dict_of_this_weeks_workouts[now] = todays_workouts
        
    date_to_check = now + timezone.timedelta(days=1)
    while date_to_check < end_of_week:
        query_of_date = WorkoutInstance.objects.filter(current_user=request.user,
                                           dates_to_be_completed__date_completed=date_to_check).exclude(
                                                   youngest_scheduled_date=None).distinct().order_by('-youngest_scheduled_date', 'date_added_by_user')
        if query_of_date:
            dict_of_this_weeks_workouts[date_to_check] = query_of_date
        date_to_check += timezone.timedelta(days=1)

    yesterday = now - timezone.timedelta(days=1)
    workouts_with_no_results_yesterday = WorkoutInstance.objects.filter(current_user=request.user,
                                                                        dates_to_be_completed__date_completed=yesterday).exclude(
                                                                            dates_workout_completed__date_completed=yesterday).distinct().order_by('-youngest_scheduled_date')

    context = {
        'users_workouts': users_workouts,
        'long_future_workouts': long_future_workouts,
        'recent_past_workouts': recent_past_workouts,
        'long_past_workouts': long_past_workouts,
        'other_workouts': other_workouts,
        'dict_of_this_weeks_workouts': dict_of_this_weeks_workouts,
        'workouts_with_no_results_yesterday': workouts_with_no_results_yesterday,
        'request_list': request_list,
        }

    if Athlete.objects.filter(user=request.user):
        coaches = request.user.athlete.coach_set.all()
        context['coaches'] = coaches
        
    if request.user.is_coach or request.user.is_gym_owner:
        athletes = request.user.coach.athletes.all()
        gym_owner = request.user.athlete.gym_owner
        groups = request.user.coach.group_set.all()
        
        all_workouts_from_all_athletes = []
        for i in athletes:
            all_workouts_from_all_athletes += i.user.workoutinstance_set.all()

        context['athletes'] = athletes
        context['gym_owner'] = gym_owner
        context['groups'] = groups
        context['all_workouts_from_all_athletes'] = all_workouts_from_all_athletes #currently not used in template
        
    return render(request, 'metcons/user_page.html', context=context)

@login_required
def add_athletes_to_coach(request, username):
    user = User.objects.get(username=username)

    if request.method == 'POST':
        if 'add athlete by username' in request.POST:
            form = AddAthleteToCoachForm(request.POST)
            if form.is_valid():
                user_athlete_to_add = User.objects.get(username=form.cleaned_data['athlete_username'])
                user_athlete_to_add_profile = Athlete.objects.get(user=user_athlete_to_add)
                
                #change this to send a notification to the athlete. once the athlete accepts then add to coach and athlete
                Request.objects.create(requestee=user_athlete_to_add, requestor=user, is_adding_athlete=True)
##                user.coach.athletes.add(user_athlete_to_add_profile)

                return HttpResponseRedirect(reverse('profile', args=[request.user.username]))

    else:
        form = AddAthleteToCoachForm()

    context = {
        'form': form,
        }

    return render(request, 'metcons/add_athlete_page.html', context=context)

@login_required
def remove_athletes_from_coach(request, username):
    coach_user = request.user
    athletes = coach_user.coach.athletes.all()

    if request.method == 'POST':
        if 'remove athletes from coach' in request.POST:
            form = RemoveAthleteFromCoachForm(request.POST)
            athlete_to_remove = request.POST.getlist('athlete_to_remove')
            form.fields['athlete_to_remove'].choices = [(i, i) for i in athlete_to_remove]
            if form.is_valid():
                for i in form.cleaned_data['athlete_to_remove']:
                    user = User.objects.get(username=i)
                    if coach_user.coach.group_set.filter(athletes=user.athlete).exists():
                        for group in coach_user.coach.group_set.filter(athletes=user.athlete):
                            group.athletes.remove(user.athlete)
                            if not group.athletes.all():
                                group.delete()
                    coach_user.coach.athletes.remove(user.athlete)

                return HttpResponseRedirect(reverse('profile', args=[request.user.username]))

    else:
        form = RemoveAthleteFromCoachForm()
        if request.user.is_coach or request.user.is_gym_owner:
            form.fields['athlete_to_remove'].choices = [(athlete.user.username, athlete.user.username) for athlete in athletes]

    context = {
        'form': form,
        'athletes': athletes,
        }

    return render(request, 'metcons/remove_athletes_from_coach.html', context=context)

@login_required
def create_group(request, username):
    user = request.user
    athletes = user.coach.athletes.all()

    if request.method == 'POST':
        if 'create group' in request.POST:
            form = CreateGroupForm(request.POST)
            athlete_to_add = request.POST.getlist('athlete_to_add')
            form.fields['athlete_to_add'].choices = [(i, i) for i in athlete_to_add]
            if form.is_valid():
                if not Group.objects.filter(name=form.cleaned_data['group_name'], coach=user.coach):
                    group = Group(name=form.cleaned_data['group_name'],
                                  coach=user.coach)
                    group.save()

                    for i in form.cleaned_data['athlete_to_add']:
                        user = User.objects.get(username=i)
                        group.athletes.add(user.athlete)

                    return HttpResponseRedirect(reverse('group_detail', args=[request.user.username, group.id]))
                else:
                    group = Group.objects.get(name=form.cleaned_data['group_name'], coach=user.coach)

                    return HttpResponseRedirect(reverse('group_detail', args=[request.user.username, group.id]))
    else:
        form = CreateGroupForm()
        if request.user.is_coach or request.user.is_gym_owner:
            form.fields['athlete_to_add'].choices = [(athlete.user.username, athlete.user.username) for athlete in athletes]

    context = {
        'form': form,
        'athletes': athletes,
        }

    return render(request, 'metcons/create_group.html', context=context)

@login_required
def group_detail(request, username, pk):
    user = request.user
    group = Group.objects.get(id=pk)
    athletes_in_group = group.athletes.all()

    context = {
        'group': group,
        'athletes_in_group': athletes_in_group,
        }

    return render(request, 'metcons/group_detail.html', context=context)

@login_required
def delete_group(request, username, pk):
    user = request.user
    group = Group.objects.get(id=pk)

    if request.method == "POST":
        if 'yes, delete group' in request.POST:
            group.delete()

        return HttpResponseRedirect(reverse('profile', args=[request.user.username]))

    context = {
        'group': group,
        }

    return render(request, 'metcons/delete_group.html', context=context)
                
@login_required
def add_athletes_to_group(request, username, pk):
    user = request.user
    group = Group.objects.get(id=pk)
    athletes_not_already_in_group = user.coach.athletes.filter(~Q(group=group))

    if request.method == 'POST':
        if 'add athletes to group' in request.POST:
            form = AddAthletesToGroupForm(request.POST)
            athlete_to_add = request.POST.getlist('athlete_to_add')
            form.fields['athlete_to_add'].choices = [(i, i) for i in athlete_to_add]
            if form.is_valid():
                for i in form.cleaned_data['athlete_to_add']:
                    user = User.objects.get(username=i)
                    group.athletes.add(user.athlete)

                return HttpResponseRedirect(reverse('group_detail', args=[request.user.username, group.id]))

    else:
        form = AddAthletesToGroupForm()
        if request.user.is_coach or request.user.is_gym_owner:
            form.fields['athlete_to_add'].choices = [(athlete.user.username, athlete.user.username) for athlete in athletes_not_already_in_group]

    context = {
        'form': form,
        'group': group,
        'athletes_not_already_in_group': athletes_not_already_in_group,
        }

    return render(request, 'metcons/add_athletes_to_group.html', context=context)

@login_required
def remove_athletes_from_group(request, username, pk):
    user = request.user
    group = Group.objects.get(id=pk)
    athletes_in_group = group.athletes.all()

    if request.method == 'POST':
        if 'remove athletes from group' in request.POST:
            form = RemoveAthletesFromGroupForm(request.POST)
            athlete_to_remove = request.POST.getlist('athlete_to_remove')
            form.fields['athlete_to_remove'].choices = [(i, i) for i in athlete_to_remove]
            if form.is_valid():
                for i in form.cleaned_data['athlete_to_remove']:
                    user = User.objects.get(username=i)
                    group.athletes.remove(user.athlete)
                    if not group.athletes.all():
                        group.delete()
                        return HttpResponseRedirect(reverse('profile', args=[request.user.username]))

                return HttpResponseRedirect(reverse('group_detail', args=[request.user.username, group.id]))

    else:
        form = RemoveAthletesFromGroupForm()
        if request.user.is_coach or request.user.is_gym_owner:
            form.fields['athlete_to_remove'].choices = [(athlete.user.username, athlete.user.username) for athlete in athletes_in_group]

    context = {
        'form': form,
        'group': group,
        'athletes_in_group': athletes_in_group,
        }

    return render(request, 'metcons/remove_athletes_from_group.html', context=context)

@login_required
def add_coach(request, username):
    athlete_user = User.objects.get(username=username)
    athlete_user_athlete_profile = Athlete.objects.get(user=athlete_user)

    if request.method == 'POST':
        if 'add coach by username' in request.POST:
            form = AddCoachForm(request.POST)
            if form.is_valid():
                coach_to_add = User.objects.get(username=form.cleaned_data['coach_username'])
                coach_to_add_coach_profile = Coach.objects.get(user=coach_to_add)
                
                #send a notification to the coach and once they accept then add to both
                Request.objects.create(requestee=coach_to_add, requestor = athlete_user, is_adding_coach=True)
##                coach_to_add_coach_profile.athletes.add(athlete_user_athlete_profile)
##                coach_to_add_coach_profile.save()

                return HttpResponseRedirect(reverse('profile', args=[request.user.username]))

    else:
        form = AddCoachForm()

    context = {
        'form': form,
        'athlete_user': athlete_user,
        }

    return render(request, 'metcons/add_coach_page.html', context=context)

@login_required
def remove_coaches_from_athlete(request, username):
    athlete_user = request.user
    coaches = athlete_user.athlete.coach_set.all()

    if request.method == 'POST':
        if 'remove coaches from athlete' in request.POST:
            form = RemoveCoachFromAthleteForm(request.POST)
            coach_to_remove = request.POST.getlist('coach_to_remove')
            form.fields['coach_to_remove'].choices = [(i, i) for i in coach_to_remove]
            if form.is_valid():
                for i in form.cleaned_data['coach_to_remove']:
                    coach_user = User.objects.get(username=i)
                    coach_user.coach.athletes.remove(athlete_user.athlete)

                return HttpResponseRedirect(reverse('profile', args=[request.user.username]))

    else:
        form = RemoveCoachFromAthleteForm()
        form.fields['coach_to_remove'].choices = [(coach.user.username, coach.user.username) for coach in coaches]

    context = {
        'form': form,
        'coaches': coaches,
        }

    return render(request, 'metcons/remove_coaches_from_athlete.html', context=context)

@login_required
def request_list_view(request, username):
    user = User.objects.get(username=username)
    request_list = Request.objects.filter(requestee=request.user)

    context = {
        'request_list': request_list,
        }

    return render(request, 'metcons/request_list.html', context=context)

@login_required
def request_detail(request, username, pk):
    user = User.objects.get(username=username)
    specific_request = Request.objects.get(id=pk, requestee=request.user)

    if request.method == 'POST':
        if 'confirm' in request.POST:
            specific_request.is_confirmed=True
            specific_request.save()
            if specific_request.is_adding_athlete:
                coach_user = specific_request.requestor
                coach_user_profile = coach_user.coach
                athlete_user = specific_request.requestee
                athlete_user_profile = athlete_user.athlete
                coach_user_profile.athletes.add(athlete_user_profile)
            elif specific_request.is_adding_coach:
                athlete_user = specific_request.requestor
                athlete_user_profile = athlete_user.athlete
                coach_user = specific_request.requestee
                coach_user_profile = coach_user.coach
                coach_user_profile.athletes.add(athlete_user_profile)
        elif 'deny' in request.POST:
            specific_request.delete()

        return HttpResponseRedirect(reverse('profile', args=[request.user.username]))
        

    context = {
        'specific_request': specific_request,
        }

    return render(request, 'metcons/request_detail.html', context=context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            if form.cleaned_data['athlete_status'] == 'G':
                user.is_gym_owner = True
                user.is_coach = True
                GymOwner.objects.create(user=user)
                Coach.objects.create(user=user)
            elif form.cleaned_data['athlete_status'] == 'C':
                user.is_coach = True
                Coach.objects.create(user=user)
            user.is_athlete = True
            user.user_gender = form.cleaned_data['gender']
            user.workout_default_gender = form.cleaned_data['default_workout_gender']
            user.save()
            Athlete.objects.create(user=user)
            username = form.cleaned_data['username']
            raw_password = form.cleaned_data['password1']
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return HttpResponseRedirect(reverse('profile', args=[request.user.username]))

    else:
        form = SignUpForm()

    context = {
        'form': form,
        }
    
    return render(request, 'metcons/signup.html', context=context)

@login_required
def profileredirect(request):
    return HttpResponseRedirect(reverse('profile', args=[request.user.username]))

def workoutlistview(request):
    # default object list excludes users workouts that have been completed and workouts that were created by other users.
    object_list = Workout.objects.all()
    now = timezone.localtime(timezone.now()).date()
    
    query1 = request.GET.getlist('q')
    query2 = request.GET.get('z')
    query3 = request.GET.get('x')
    query4 = request.GET.get('y')
    query5 = request.GET.get('t')
    query6 = request.GET.get('s')
    query7 = request.GET.get('f')
    query8 = request.GET.get('h')
    
    if User.objects.filter(username = request.user.username).exists():
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
            current_users_completed_instances = WorkoutInstance.objects.filter(current_user=request.user, dates_workout_completed__isnull=False)
            object_list = object_list.exclude(workoutinstance__id__in=current_users_completed_instances)
        if query8:
            #add an exclude to this to not show workouts that people have marked private later on
            query7 = 'on'
            object_list = object_list.filter(workoutinstance__current_user__username = query8)
        if not query7:
            object_list = object_list.exclude(~Q(created_by_user=request.user),
                                              where_workout_came_from='Gym Owner Created').exclude(
                                                  ~Q(created_by_user=request.user),
                                                  where_workout_came_from='Coach Created').exclude(
                                                      ~Q(created_by_user=request.user),
                                                      where_workout_came_from='Athlete Created')

    paginator = Paginator(object_list, 10)
    page = request.GET.get('page', 1)
    workout_list = paginator.page(page)            

    context = {
        'workout_list': workout_list,
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
                                           duration_in_seconds=workout.estimated_duration_in_seconds,
                                           edited_workout_text=workout.workout_text,
                                           edited_scaling_text=workout.scaling_or_description_text)
                instance.save()
            else:
                instance = WorkoutInstance.objects.get(workout=workout, current_user=current_user)
            return HttpResponseRedirect(reverse('interim_created_workout', args=[request.user.username, instance.id]))
        
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
                                           duration_in_seconds=workout.estimated_duration_in_seconds,
                                           edited_workout_text=workout.workout_text,
                                           edited_scaling_text=workout.scaling_or_description_text)
                instance.save()
            else:
                instance = WorkoutInstance.objects.get(workout=workout, current_user=current_user)
            return HttpResponseRedirect(reverse('interim_created_workout', args=[request.user.username, instance.id]))
    
    return render(request, 'metcons/workout_detail.html', context=context)

@login_required
def workoutinstancedetailview(request, username, pk):
    instance = WorkoutInstance.objects.get(id=pk)

    if instance.duration_in_seconds:
        duration_minutes = (instance.duration_in_seconds // 60)
        duration_seconds = instance.duration_in_seconds % 60
    else:
        duration_minutes = 0
        duration_seconds = 0
    result_list = Result.objects.filter(workoutinstance=instance).order_by('-date_workout_completed', '-date_created')

    if request.method == 'POST':
        if request.user.is_coach or request.user.is_gym_owner:
            if 'unhide instance' in request.POST:
                instance.is_hidden = False
                instance.date_to_unhide = None
                instance.save()
                
                return HttpResponseRedirect(instance.get_absolute_url())

    paginator = Paginator(result_list, 5)
    page = request.GET.get('page', 1)
    result_list = paginator.page(page)
    
    context = {
        'duration_minutes': duration_minutes,
        'duration_seconds': duration_seconds,
        'result_list': result_list,
        'workoutinstance': instance,
        'workout': instance.workout,
        }

    return render(request, 'metcons/workoutinstance_detail.html', context=context)

class MovementListView(generic.ListView):
    model = Movement
    paginate_by = 20

class MovementDetailView(generic.DetailView):
    model = Movement

@login_required
def schedule_instance(request, username, pk):
    instance = WorkoutInstance.objects.get(id=pk)
    if request.method == 'POST':
        if 'schedule instance' in request.POST:
            form = ScheduleInstanceForm(request.POST)
            if form.is_valid():
                if form.cleaned_data['date_to_be_added'] == dt.date.today():
                    aware_datetime = timezone.now()
                else:
                    date_in_datetime = dt.datetime.combine(form.cleaned_data['date_to_be_added'], dt.datetime.min.time())
                    aware_datetime = timezone.make_aware(date_in_datetime)
                local_date = timezone.localtime(aware_datetime).date()
                list_of_dates_to_schedule=[local_date]
                if form.cleaned_data['repeat_yes'] == True:
                    repeat_frequency = int(form.cleaned_data['repeat_frequency'])
                    number_of_repetitions = form.cleaned_data['number_of_repetitions']
                    repeat_length = int(form.cleaned_data['repeat_length'])
                    end_repeat_scheduling_date = local_date + timezone.timedelta(days=number_of_repetitions*repeat_length)
                    list_of_dates_to_schedule = []
                    while local_date <= end_repeat_scheduling_date:
                        list_of_dates_to_schedule.append(local_date)
                        local_date += timezone.timedelta(days=repeat_frequency)

                instance.add_date_to_be_completed(*list_of_dates_to_schedule)

                return HttpResponseRedirect(reverse('profile', args=[request.user.username]))
    else:
        form = ScheduleInstanceForm()
        if 'schedule workout for future' in request.GET:
            tomorrow = timezone.localtime(timezone.now()).date() + timezone.timedelta(days=1)
            form.fields['date_to_be_added'].initial = tomorrow

    context = {
        'form': form,
        'instance': instance,
        }

    return render(request, 'metcons/schedule_instance.html', context)

@login_required
def schedule_instance_for_multiple_athletes(request, username, pk):
    workout = Workout.objects.get(id=pk)
    user = request.user
    athletes = user.coach.athletes.filter(user__workoutinstance__workout=workout)

    if request.method == 'POST':
        if 'schedule for all athletes' in request.POST:
            form = ScheduleInstanceForm(request.POST)
            if form.is_valid():
                if form.cleaned_data['date_to_be_added'] == dt.date.today():
                    aware_datetime = timezone.now()
                else:
                    date_in_datetime = dt.datetime.combine(form.cleaned_data['date_to_be_added'], dt.datetime.min.time())
                    aware_datetime = timezone.make_aware(date_in_datetime)
                local_date = timezone.localtime(aware_datetime).date()
                list_of_dates_to_schedule=[local_date]
                if form.cleaned_data['repeat_yes'] == True:
                    repeat_frequency = int(form.cleaned_data['repeat_frequency'])
                    number_of_repetitions = form.cleaned_data['number_of_repetitions']
                    repeat_length = int(form.cleaned_data['repeat_length'])
                    end_repeat_scheduling_date = local_date + timezone.timedelta(days=number_of_repetitions*repeat_length)
                    list_of_dates_to_schedule = []
                    while local_date <= end_repeat_scheduling_date:
                        list_of_dates_to_schedule.append(local_date)
                        local_date += timezone.timedelta(days=repeat_frequency)

                if athletes:
                    for i in athletes:
                        instance = WorkoutInstance.objects.get(current_user=i.user, workout=workout)
                        instance.add_date_to_be_completed(*list_of_dates_to_schedule)

                    return HttpResponseRedirect(reverse('profile', args=[request.user.username]))

    else:
        form = ScheduleInstanceForm()
        if 'schedule workout for future' in request.GET:
            tomorrow = timezone.localtime(timezone.now()).date() + timezone.timedelta(days=1)
            form.fields['date_to_be_added'].initial = tomorrow

    context = {
        'form': form,
        'workout': workout,
        'athletes': athletes,
        }

    return render(request, 'metcons/schedule_instance_for_multiple_athletes.html', context)

@login_required
def edit_schedule(request, username, pk):
    instance = WorkoutInstance.objects.get(id=pk)
    now = timezone.localtime(timezone.now()).date()
    yesterday = now - timezone.timedelta(days=1)
    future_dates_plus_yesterday = instance.dates_to_be_completed.filter(date_completed__gte=yesterday)
    
    if request.method == 'POST':
        if 'edit schedule' in request.POST:
            form = EditScheduleForm(request.POST)
            date_to_be_removed = request.POST.getlist('date_to_be_removed')
            form.fields['date_to_be_removed'].choices = [(i, i) for i in date_to_be_removed]
            if form.is_valid():
                i=0
                dates_to_be_removed = []
                while i < len(date_to_be_removed):
                    date_in_datetime = dt.datetime.strptime(form.cleaned_data['date_to_be_removed'][i], "%Y-%m-%d")
                    aware_datetime = timezone.make_aware(date_in_datetime)
                    local_date_to_be_removed = timezone.localtime(aware_datetime).date()
                    dates_to_be_removed.append(local_date_to_be_removed)
                    i+=1
                
                if form.cleaned_data['date_to_be_added'] == dt.date.today():
                    aware_datetime = timezone.now()
                else:
                    date_in_datetime = dt.datetime.combine(form.cleaned_data['date_to_be_added'], dt.datetime.min.time())
                    aware_datetime = timezone.make_aware(date_in_datetime)
                local_date_to_be_added = timezone.localtime(aware_datetime).date()

                if dates_to_be_removed:
                    instance.remove_date_to_be_completed(*dates_to_be_removed)
                if local_date_to_be_added:
                    instance.add_date_to_be_completed(local_date_to_be_added)

                return HttpResponseRedirect(reverse('profile', args=[request.user.username]))

    else:
        now = timezone.localtime(timezone.now()).date()
        form = EditScheduleForm()
        if future_dates_plus_yesterday:
            form.fields['date_to_be_removed'].choices = [(date.date_completed, date.date_completed) for date in instance.dates_to_be_completed.filter(date_completed__gte=now)]
        else:
            form.fields.pop('date_to_be_removed')
        if 'previous day edit schedule' in request.GET:
            yesterday = now - timezone.timedelta(days=1)
            form.fields['date_to_be_removed'].choices = [(date.date_completed, date.date_completed) for date in instance.dates_to_be_completed.filter(date_completed__gte=yesterday)]
            form.fields['date_to_be_removed'].initial = yesterday
            form.fields['date_to_be_added'].initial = now

    context = {
        'form': form,
        'instance': instance,
        'future_dates_plus_yesterday': future_dates_plus_yesterday,
        }
    
    return render(request, 'metcons/edit_schedule.html', context)

@login_required
def edit_schedule_for_multiple_athletes(request, username, pk):
    workout = Workout.objects.get(id=pk)
    user = request.user
    athletes = user.coach.athletes.filter(user__workoutinstance__workout=workout)

    if request.method == 'POST':
        if 'edit schedule for all athletes' in request.POST:
            form = EditScheduleForm(request.POST)
            date_to_be_removed = request.POST.getlist('date_to_be_removed')
            form.fields['date_to_be_removed'].choices = [(i, i) for i in date_to_be_removed]
            if form.is_valid():
                i=0
                dates_to_be_removed = []
                while i < len(date_to_be_removed):
                    date_in_datetime = dt.datetime.strptime(form.cleaned_data['date_to_be_removed'][i], "%Y-%m-%d")
                    aware_datetime = timezone.make_aware(date_in_datetime)
                    local_date_to_be_removed = timezone.localtime(aware_datetime).date()
                    dates_to_be_removed.append(local_date_to_be_removed)
                    i+=1
                
                if form.cleaned_data['date_to_be_added'] == dt.date.today():
                    aware_datetime = timezone.now()
                else:
                    date_in_datetime = dt.datetime.combine(form.cleaned_data['date_to_be_added'], dt.datetime.min.time())
                    aware_datetime = timezone.make_aware(date_in_datetime)
                local_date_to_be_added = timezone.localtime(aware_datetime).date()

                if athletes:
                    for i in athletes:
                        instance = WorkoutInstance.objects.get(current_user=i.user, workout=workout)
                        if dates_to_be_removed:
                            instance.remove_date_to_be_completed(*dates_to_be_removed)
                        if local_date_to_be_added:
                            instance.add_date_to_be_completed(local_date_to_be_added)

                    return HttpResponseRedirect(reverse('profile', args=[request.user.username]))

    else:
        form = EditScheduleForm()
        now = timezone.localtime(timezone.now()).date()
        yesterday = now - timezone.timedelta(days=1)
        workout_scheduled_dates = []
        for i in athletes:
            instance = i.user.workoutinstance_set.get(workout=workout)
            for date in instance.dates_to_be_completed.filter(date_completed__gte=yesterday):
                if date not in workout_scheduled_dates:
                    workout_scheduled_dates.append(date)
        if workout_scheduled_dates:
            form.fields['date_to_be_removed'].choices = [(date.date_completed, date.date_completed) for date in workout_scheduled_dates]
        else:
            form.fields.pop('date_to_be_removed')
        if 'previous day edit schedule' in request.GET:
            form.fields['date_to_be_removed'].initial = yesterday
            form.fields['date_to_be_added'].initial = now

    context = {
        'form': form,
        'workout': workout,
        'athletes': athletes,
        'workout_scheduled_dates': workout_scheduled_dates,
        }

    return render(request, 'metcons/edit_schedule_for_multiple_athletes.html', context)

@login_required
def delete_schedule(request, username, pk):
    instance = WorkoutInstance.objects.get(id=pk)
    now = timezone.localtime(timezone.now()).date()
    future_dates = instance.dates_to_be_completed.filter(date_completed__gte=now)
    
    if request.method == 'POST':
        if 'delete schedule' in request.POST:
            form = DeleteScheduleForm(request.POST)
            date_to_be_removed = request.POST.getlist('date_to_be_removed')
            form.fields['date_to_be_removed'].choices = [(i, i) for i in date_to_be_removed]
            if form.is_valid():
                i=0
                dates_to_be_removed = []
                while i < len(date_to_be_removed):
                    date_in_datetime = dt.datetime.strptime(form.cleaned_data['date_to_be_removed'][i], "%Y-%m-%d")
                    aware_datetime = timezone.make_aware(date_in_datetime)
                    local_date_to_be_removed = timezone.localtime(aware_datetime).date()
                    dates_to_be_removed.append(local_date_to_be_removed)
                    i+=1

                instance.remove_date_to_be_completed(*dates_to_be_removed)

                return HttpResponseRedirect(reverse('profile', args=[request.user.username]))

    else:
        form = DeleteScheduleForm()
        form.fields['date_to_be_removed'].choices = [(date.date_completed, date.date_completed) for date in instance.dates_to_be_completed.filter(date_completed__gte=now)]
        #not sure if I want to have an initial choice here.
        #form.fields['date_to_be_removed'].initial = instance.youngest_scheduled_date.date_completed

    context = {
        'form': form,
        'instance': instance,
        'future_dates': future_dates,
        }
    
    return render(request, 'metcons/delete_schedule.html', context)

@login_required
def hide_instance(request, username, pk):
    instance = WorkoutInstance.objects.get(id=pk)

    if request.method == 'POST':
        if 'hide instance' in request.POST:
            form = HideInstanceForm(request.POST)
            if form.is_valid():
                if instance.is_assigned_by_coach_or_gym_owner:
                    instance.is_hidden=True
                    if form.cleaned_data['date_to_unhide']:
                        instance.date_to_unhide = form.cleaned_data['date_to_unhide']
                    else:
                        instance.date_to_unhide = None

                    instance.save()

                return HttpResponseRedirect(instance.get_absolute_url())

    form = HideInstanceForm()

    context = {
        'form': form,
        'instance': instance,
        }

    return render(request, 'metcons/hide_instance.html', context=context)

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
        if request.user == instance.current_user or request.user.coach in instance.current_user.athlete.coach_set.all():
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
                    for i in request.FILES.getlist('media_file'):
                        resultfile = ResultFile(result=result,
                                            caption = form.cleaned_data['media_file_caption'],
                                            file=i,
                                            content_type = i.content_type)
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
        if 'created workout today add result' in request.GET:
            now = timezone.localtime(timezone.now()).date()
            form.fields['date_completed'].initial = now
        elif 'previous day add result' in request.GET or 'created workout previous day add result' in request.GET:
            yesterday = timezone.localtime(timezone.now()).date() - timezone.timedelta(days=1)
            form.fields['date_completed'].initial = yesterday

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
            if request.user == instance.current_user or request.user.coach in instance.current_user.athlete.coach_set.all():
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
def add_workout_to_athletes(request, username, pk):
    workout = Workout.objects.get(id=pk)
    user = request.user
    athletes = user.coach.athletes.all()
    groups = user.coach.group_set.all()

    if request.method == 'POST':
        if user.is_coach or user.is_gym_owner:
            form = AddWorkoutToAthletesForm(request.POST)
            athlete_to_assign = request.POST.getlist('athlete_to_assign')
            form.fields['athlete_to_assign'].choices = [(i, i) for i in athlete_to_assign]
            group_to_assign = request.POST.getlist('group_to_assign')
            form.fields['group_to_assign'].choices = [(i, i) for i in group_to_assign]
            if form.is_valid():
                if form.cleaned_data['hide_from_athletes']:
                    hidden=True
                    date_to_unhide = form.cleaned_data['date_to_unhide']
                else:
                    hidden=False
                    date_to_unhide = None
                if form.cleaned_data['athlete_to_assign']:
                    for i in form.cleaned_data['athlete_to_assign']:
                        current_user = User.objects.get(username=i)
                        if not WorkoutInstance.objects.filter(workout=workout, current_user=current_user):
                            instance = WorkoutInstance(workout=workout, current_user=current_user,
                                                       duration_in_seconds=workout.estimated_duration_in_seconds,
                                                       edited_workout_text=workout.workout_text,
                                                       edited_scaling_text=workout.scaling_or_description_text,
                                                       is_assigned_by_coach_or_gym_owner=True,
                                                       assigned_by_user=user,
                                                       is_hidden=hidden,
                                                       date_to_unhide=date_to_unhide)
                            instance.save()
                if form.cleaned_data['group_to_assign']:
                    for i in form.cleaned_data['group_to_assign']:
                        group = Group.objects.get(name=i, coach=user.coach)
                        for i in group.athletes.all():
                            current_user = i.user
                            if not WorkoutInstance.objects.filter(workout=workout, current_user=current_user):
                                instance = WorkoutInstance(workout=workout, current_user=current_user,
                                                           duration_in_seconds=workout.estimated_duration_in_seconds,
                                                           edited_workout_text=workout.workout_text,
                                                           edited_scaling_text=workout.scaling_or_description_text,
                                                           is_assigned_by_coach_or_gym_owner=True,
                                                           assigned_by_user=user,
                                                           is_hidden=hidden,
                                                           date_to_unhide=date_to_unhide)
                                instance.save()

                return HttpResponseRedirect(reverse('interim_created_workout_for_multiple_athletes', args=[request.user.username, workout.id]))

    else:
        form = AddWorkoutToAthletesForm()
        if request.user.is_coach or request.user.is_gym_owner:
            form.fields['athlete_to_assign'].choices = [(athlete.user.username, athlete.user.username) for athlete in athletes]
            if groups:
                form.fields['group_to_assign'].choices = [(group.name, group.name) for group in groups]
            else:
                form.fields.pop('group_to_assign')
            
    context = {
        'form': form,
        'athletes': athletes,
        'groups': groups,
        }

    return render(request, 'metcons/add_workout_to_athletes.html', context)
            
@login_required    
def create_workout(request):
    """View function for creating a new workout"""

    if request.method == 'POST':
        form = CreateWorkoutForm(request.POST, **{'user':request.user})
        if request.user.is_coach or request.user.is_gym_owner:
            athlete_to_assign = request.POST.getlist('athlete_to_assign')
            form.fields['athlete_to_assign'].choices = [(i, i) for i in athlete_to_assign]
            group_to_assign = request.POST.getlist('group_to_assign')
            form.fields['group_to_assign'].choices = [(i, i) for i in group_to_assign]
        if form.is_valid():
            current_user = User.objects.get(username=request.user.username)
            users_to_assign_workout = []
            if current_user.is_coach or current_user.is_gym_owner:
                if form.cleaned_data['athlete_to_assign']:
                    for i in form.cleaned_data['athlete_to_assign']:
                        user = User.objects.get(username=i)
                        users_to_assign_workout.append(user)
                if form.cleaned_data['group_to_assign']:
                    for i in form.cleaned_data['group_to_assign']:
                        group = Group.objects.get(name=i, coach=current_user.coach)
                        for i in group.athletes.all():
                            users_to_assign_workout.append(i.user)
                if not form.cleaned_data['athlete_to_assign'] and not form.cleaned_data['group_to_assign']:
                    users_to_assign_workout.append(current_user)
            else:
                users_to_assign_workout.append(current_user)
            if not Workout.objects.filter(workout_text=form.cleaned_data['workout_text']):
                if current_user.is_gym_owner:
                    workout_location = 'Gym Owner Created'
                elif current_user.is_coach:
                    workout_location = 'Coach Created'
                else:
                    workout_location = 'Athlete Created'
                if form.cleaned_data['estimated_duration']:
                    estimated_duration = form.cleaned_data['estimated_duration'] * 60
                else:
                    estimated_duration = None
                workout = Workout(workout_text=form.cleaned_data['workout_text'],
                                  scaling_or_description_text=form.cleaned_data['workout_scaling'],
                                  estimated_duration_in_seconds=estimated_duration,
                                  where_workout_came_from=workout_location,
                                  classification=None,
                                  created_by_user = current_user,
                                  gender = form.cleaned_data['gender'],
                                  )
                workout.save()
                if Workout.objects.filter(id=workout.id, workout_text__iregex=r'as possible in \d+ minutes of'):
                    r1=re.findall(r'as possible in \d+ minutes of', workout.workout_text)
                    workout.estimated_duration_in_seconds=int(re.split('\s', r1[0])[3])
                workout.update_movements_and_classification()

            else:
                workout = Workout.objects.get(workout_text=form.cleaned_data['workout_text'])

            if (request.user.is_coach and form.cleaned_data['hide_from_athletes?']) or (request.user.is_gym_owner and form.cleaned_data['hide_from_athletes?']):
                hidden=True
                date_to_unhide = form.cleaned_data['date_to_unhide']
            else:
                hidden=False
                date_to_unhide = None
                    
            for i in users_to_assign_workout:
                if not WorkoutInstance.objects.filter(workout=workout, current_user=i):
                    if i != request.user:
                        assigned = True
                    else:
                        assigned = False
                    instance = WorkoutInstance(workout=workout, current_user = i,
                                               duration_in_seconds=workout.estimated_duration_in_seconds,
                                               edited_workout_text=workout.workout_text,
                                               edited_scaling_text=workout.scaling_or_description_text,
                                               is_assigned_by_coach_or_gym_owner=assigned)
                    instance.save()
                    if instance.is_assigned_by_coach_or_gym_owner:
                        instance.is_hidden=hidden
                        instance.date_to_unhide=date_to_unhide
                        instance.assigned_by_user=current_user
                        instance.save()
                else:
                    instance = WorkoutInstance.objects.get(workout=workout, current_user=i)

            if len(users_to_assign_workout) > 1:
                return HttpResponseRedirect(reverse('interim_created_workout_for_multiple_athletes', args=[request.user.username, workout.id]))
            else:
                return HttpResponseRedirect(reverse('interim_created_workout', args=[request.user.username, instance.id]))

    else:
        form = CreateWorkoutForm(**{'user':request.user}, initial={'gender': request.user.workout_default_gender,
                                          })
        if request.user.is_coach or request.user.is_gym_owner:
            if request.user.coach.athletes.all():
                form.fields['athlete_to_assign'].choices = [(athlete.user.username, athlete.user.username) for athlete in request.user.coach.athletes.all()]
            else:
                form.fields.pop('athlete_to_assign')
                form.fields.pop('hide_from_athletes?')
                form.fields.pop('date_to_unhide')
            if request.user.coach.group_set.all():
                form.fields['group_to_assign'].choices = [(group.name, group.name) for group in request.user.coach.group_set.all()]
            else:
                form.fields.pop('group_to_assign')
            
    context = {
        'form': form,
        }

    return render(request, 'metcons/create_workout.html', context)


@login_required
def interim_created_workout(request, username, pk):
    user = request.user
    instance = WorkoutInstance.objects.get(id=pk)

    if request.method == 'POST':
        if user == instance.current_user or user.coach in instance.current_user.athlete.coach_set.all():
            if 'schedule workout for today' in request.POST:
                now = timezone.localtime(timezone.now()).date()
                instance.add_date_to_be_completed(now)

                return HttpResponseRedirect(reverse('profile', args=[request.user.username]))

    context = {
        'instance': instance,
        }
    return render(request, 'metcons/interim_created_workout.html', context)

@login_required
def interim_created_workout_for_multiple_athletes(request, username, pk):
    user = request.user
    workout = Workout.objects.get(id=pk)
    athletes = user.coach.athletes.filter(user__workoutinstance__workout=workout)

    if request.method == 'POST':
        if user.is_coach:
            if 'schedule workout for today for multiple athletes' in request.POST:
                now = timezone.localtime(timezone.now()).date()
                if athletes:
                    for i in athletes:
                        instance = WorkoutInstance.objects.get(current_user=i.user, workout=workout)
                        instance.add_date_to_be_completed(now)

                    return HttpResponseRedirect(reverse('profile', args=[request.user.username]))

    context = {
        'athletes': athletes,
        'workout': workout,
        }
    return render(request, 'metcons/interim_created_workout_for_multiple_athletes.html', context)

class MovementCreate(LoginRequiredMixin, CreateView):
    model = Movement
    fields = '__all__'
