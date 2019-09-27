from django import forms
from django.forms import formset_factory
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from metcons.models import User, Movement, Classification, StrengthProgram

movement_choices = [(i.name, i.name) for i in Movement.objects.all()]

cardio_choices = [(i.name, i.name) for i in Movement.objects.filter(classification__name='Cardio')]

classification_choices = [(i.name, i.name) for i in Classification.objects.all()]

strength_program_choices = [(i.name, i.name) for i in StrengthProgram.objects.all()]

weight_unit_choices = [
    ('lbs', 'lbs'),
    ('kgs', 'kgs'),
    ('%', '%'),
    ]

strength_program_weight_unit_choices = [
    ('lbs', 'lbs'),
    ('kgs', 'kgs')
    ]

distance_or_time_unit_choices = [
    ('m', 'm'),
    ('ft', 'ft'),
    ('km', 'km'),
    ('mi', 'mi'),
    ('min', 'min'),
    ]

repetition_frequency_choices = [
    ('none', ''),
    (1, 'Daily'),
    (7, 'Weekly'),
    (28, 'Monthly'),
    (364, 'Yearly'),
    ]

repetition_length_choices = [
    ('none', ''),
    (1, 'Days'),
    (7, 'Weeks'),
    (28, 'Months'),
    (364, 'Years'),
    ]

workout_gender_choices = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('B', 'Both'),
    ]

user_gender_choices = [
    ('M', 'Male'),
    ('F', 'Female'),
    ]

athlete_status_choices = [
    ('A', 'Athlete'),
    ('C', 'Coach'),
    ('G', 'Gym Owner'),
    ]

day_variation_choices = [
    ('4 Day', '4 Day'),
    ('5 Day', '5 Day'),
    ('6 Day Squat', '6 Day Squat'),
    ('6 Day Deadlift', '6 Day Deadlift'),
    ]


def get_default_localtime():
    return timezone.localtime(timezone.now())

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    athlete_status = forms.ChoiceField(widget=forms.RadioSelect, choices=athlete_status_choices,
                                       help_text='Selecting Coach or Gym Owner will also sign you up as an athlete.')
    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=user_gender_choices)
    default_workout_gender = forms.ChoiceField(widget=forms.RadioSelect, choices=workout_gender_choices,
                                               help_text='What is the gender that you will most often write workouts for? This will be the default gender chosen when you create a workout; however, you can change this during creation of any workout.') 
    

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'athlete_status', 'gender', 'default_workout_gender', 'password1', 'password2', )
        
class AddAthleteToCoachForm(forms.Form):
    athlete_username = forms.CharField(max_length = 30, help_text='What is the athletes username? Lowercase letters only.')

class RemoveAthleteFromCoachForm(forms.Form):
    athlete_to_remove = forms.MultipleChoiceField(help_text='Which athletes would you like to remove?')
    
class AddCoachForm(forms.Form):
    coach_username = forms.CharField(max_length = 30, help_text='What is the coaches username? Lowercase letters only.')

class RemoveCoachFromAthleteForm(forms.Form):
    coach_to_remove = forms.MultipleChoiceField(help_text='Which coach would you like to remove?')

class AddWorkoutToAthletesForm(forms.Form):
    athlete_to_assign = forms.MultipleChoiceField(required=False, help_text='Which athletes would you like to assign this workout to?')
    group_to_assign = forms.MultipleChoiceField(required=False, help_text='Which groups would you like to assign this workout to?')
    hide_from_athletes = forms.BooleanField(required=False, help_text='Would you like to hide the details of this workout from assigned athletes until a specified date?')
    date_to_unhide = forms.DateField(required=False, widget=forms.SelectDateWidget(), initial=get_default_localtime, help_text='When would you like to unhide this workout?')

class CreateGroupForm(forms.Form):
    group_name = forms.CharField(max_length = 254)
    athlete_to_add = forms.MultipleChoiceField(help_text='Which athletes would you like to add to this group?')

class AddAthletesToGroupForm(forms.Form):
    athlete_to_add = forms.MultipleChoiceField(help_text='Which athletes would you like to add to this group?')

class RemoveAthletesFromGroupForm(forms.Form):
    athlete_to_remove = forms.MultipleChoiceField(help_text='Which athletes would you like to remove from this group?')
    
class CreateWorkoutForm(forms.Form):
    workout_text = forms.CharField(widget=forms.Textarea, max_length=2000, help_text="Enter your workout.")
    workout_scaling = forms.CharField(widget=forms.Textarea, max_length=4000, help_text='Enter any scaling options.', required=False)
    estimated_duration = forms.IntegerField(help_text='Enter an estimate of how long it will take to complete the workout in minutes (whole numbers only).', required=False)
    gender = forms.ChoiceField(widget=forms.Select(), choices=workout_gender_choices, help_text='Is this workout (and the weights you have entered) applicable for both Males and Females or only one?')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CreateWorkoutForm, self).__init__(*args, **kwargs)
        if user.is_coach or user.is_gym_owner:
            self.fields['athlete_to_assign'] = forms.MultipleChoiceField(required=False, help_text='Which athletes would you like to assign this workout to?')
            self.fields['group_to_assign'] = forms.MultipleChoiceField(required=False, help_text='Which groups would you like to assign this workout to?')
            self.fields['hide_from_athletes'] = forms.BooleanField(required=False, help_text='Would you like to hide the details of this workout from assigned athletes until a specified date?')
            self.fields['date_to_unhide'] = forms.DateField(required=False, widget=forms.SelectDateWidget(), initial=get_default_localtime, help_text='When would you like to unhide this workout?')
            
class CreateMovementForm(forms.Form):
    name = forms.CharField(max_length=200, required=True)
    classification = forms.ChoiceField(widget=forms.Select(), choices=classification_choices, help_text='What classification does this movement have?')

class CreateStrengthWorkoutForm(forms.Form):
    #modify this to allow for changing number of sets/reps/weights to be created
    movement = forms.ChoiceField(widget=forms.Select(), choices=movement_choices, help_text='What Movement would you like to perform?')
    sets = forms.IntegerField(help_text='How many sets would you like to perform?')
    reps = forms.IntegerField(help_text='If reps left blank it is assumed max possible reps should be performed.', required=False)
    weight = forms.DecimalField(min_value=0.0, max_value=99999.9, decimal_places=1, max_digits=6, required=False)
    weight_units = forms.ChoiceField(widget=forms.Select(), choices=weight_unit_choices, help_text='What units is the weight in?', required=False)
    comment = forms.CharField(widget=forms.Textarea, max_length=4000, required=False, help_text='Required rest or effort')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CreateStrengthWorkoutForm, self).__init__(*args, **kwargs)
        if user.is_coach or user.is_gym_owner:
            self.fields['athlete_to_assign'] = forms.MultipleChoiceField(required=False, help_text='Which athletes would you like to assign this workout to?')
            self.fields['group_to_assign'] = forms.MultipleChoiceField(required=False, help_text='Which groups would you like to assign this workout to?')
            self.fields['hide_from_athletes'] = forms.BooleanField(required=False, help_text='Would you like to hide the details of this workout from assigned athletes until a specified date?')
            self.fields['date_to_unhide'] = forms.DateField(required=False, widget=forms.SelectDateWidget(), initial=get_default_localtime, help_text='When would you like to unhide this workout?')

StrengthWorkoutFormset = formset_factory(CreateStrengthWorkoutForm, extra=1)

class CreateStrengthProgramForm(forms.Form):
    strength_program = forms.ChoiceField(widget=forms.Select(), choices=strength_program_choices)
    day_variation = forms.ChoiceField(widget=forms.Select(), choices=day_variation_choices, required=False)
    units = forms.ChoiceField(widget=forms.Select(), choices=strength_program_weight_unit_choices)
    bench_max = forms.IntegerField(required=False, label='Bench One Rep Max')
    main_bench_start_date = forms.DateField(widget=forms.SelectDateWidget(), initial=get_default_localtime)
    squat_max = forms.IntegerField(required=False, label='Back Squat One Rep Max')
    main_squat_start_date = forms.DateField(widget=forms.SelectDateWidget(), initial=get_default_localtime)
    ohp_max = forms.IntegerField(required=False, label='Overhead Press One Rep Max')
    main_ohp_start_date = forms.DateField(widget=forms.SelectDateWidget(), initial=get_default_localtime)
    deadlift_max = forms.IntegerField(required=False, label='Deadlift One Rep Max')
    main_deadlift_start_date = forms.DateField(widget=forms.SelectDateWidget(), initial=get_default_localtime)
    secondary_bench_start_date = forms.DateField(widget=forms.SelectDateWidget(), initial=get_default_localtime, required=False)
    secondary_squat_start_date = forms.DateField(widget=forms.SelectDateWidget(), initial=get_default_localtime, required=False)
    secondary_deadlift_start_date = forms.DateField(widget=forms.SelectDateWidget(), initial=get_default_localtime, required=False)
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CreateStrengthProgramForm, self).__init__(*args, **kwargs)
        if user.is_coach or user.is_gym_owner:
            self.fields['athlete_to_assign'] = forms.MultipleChoiceField(required=False, help_text='Which athletes would you like to assign this workout to?')
            self.fields['group_to_assign'] = forms.MultipleChoiceField(required=False, help_text='Which groups would you like to assign this workout to?')
    
class CreateCardioWorkoutForm(forms.Form):
    movement = forms.ChoiceField(widget=forms.Select(), choices=cardio_choices, help_text='What Movement would you like to perform?')
    distance = forms.IntegerField(help_text='What distance?', label='Distance/Time')
    distance_units = forms.ChoiceField(widget=forms.Select(), choices=distance_or_time_unit_choices, help_text='What units is the distance in?', required=False)
    reps = forms.IntegerField(required=False)
    rest_minutes = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'rest_input'}), required=False, label='Rest')
    rest_seconds = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'rest_input'}), required = False, label='Rest Seconds')
    pace = forms.CharField(max_length=100, required=False)
    comment = forms.CharField(widget=forms.Textarea, max_length=4000, required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CreateCardioWorkoutForm, self).__init__(*args, **kwargs)
        if user.is_coach or user.is_gym_owner:
            self.fields['athlete_to_assign'] = forms.MultipleChoiceField(required=False, help_text='Which athletes would you like to assign this workout to?')
            self.fields['group_to_assign'] = forms.MultipleChoiceField(required=False, help_text='Which groups would you like to assign this workout to?')
            self.fields['hide_from_athletes'] = forms.BooleanField(required=False, help_text='Would you like to hide the details of this workout from assigned athletes until a specified date?')
            self.fields['date_to_unhide'] = forms.DateField(required=False, widget=forms.SelectDateWidget(), initial=get_default_localtime, help_text='When would you like to unhide this workout?')

CardioWorkoutFormset = formset_factory(CreateCardioWorkoutForm, extra=0)

class CreateGeneralResultForm(forms.Form):
    result_text = forms.CharField(widget=forms.Textarea, max_length=2000, help_text="Enter your results here.", required=False)
    duration_minutes = forms.IntegerField(required = False)
    duration_seconds = forms.IntegerField(required = False)
    media_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False, help_text='Attach any pictures or videos. Hold CTRL while selecting to upload multiple files.')
    media_file_caption = forms.CharField(required=False, help_text='Caption your media file if applicable.')
    date_completed = forms.DateField(widget=forms.SelectDateWidget(), initial=get_default_localtime, required=False, help_text='When did you complete this workout?')

class CreateStrengthResultForm(forms.Form):
    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        super(CreateStrengthResultForm, self).__init__(*args, **kwargs)
        if instance.strength_workout:
            if instance.is_from_strength_program:
                if instance.current_user.strength_program.strength_program.name == 'nSuns 531 LP':
                    self.fields['reps'] = forms.IntegerField(required=True, label='Reps On Heavy Set')
                    self.fields['comments'] = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'List accessories sets, reps, and weight. Or comments on difficulty of main movements'}),
                               max_length=4000, required=False)
            else:
                for i in instance.strength_workout.strength_exercises.all():
                    field_name = 'result_text_%s' % (i.strength_exercise_number,)
                    self.fields[field_name] = forms.CharField(widget=forms.Textarea, max_length=2000, label = 'Comments',
                               help_text="Enter your results here.\nYou can leave this blank if you completed as is.\nOtherwise some examples could be: 'Failed final set', 'Did 2 extra reps each set', 'changed weight to XXX'", required=False)
                
    media_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False, help_text='Attach any pictures or videos. Hold CTRL while selecting to upload multiple files.')
    media_file_caption = forms.CharField(required=False, help_text='Caption your media file if applicable.')
    date_completed = forms.DateField(widget=forms.SelectDateWidget(), initial=get_default_localtime, required=False, help_text='When did you complete this workout?')

class CreateCardioResultForm(forms.Form):
    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        super(CreateCardioResultForm, self).__init__(*args, **kwargs)
        if instance.cardio_workout:
            for i in instance.cardio_workout.cardio_exercises.all():
                field_name = 'result_text_%s' % (i.cardio_exercise_number,)
                self.fields[field_name] = forms.CharField(widget=forms.Textarea, max_length=2000, label = 'Comments', help_text="Enter your results here.\nExamples: 'Average Pace: XX:XX', 'Failed to hit pace on rep X', 'changed rest to X:XX'", required=False)
                
    media_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False, help_text='Attach any pictures or videos. Hold CTRL while selecting to upload multiple files.')
    media_file_caption = forms.CharField(required=False, help_text='Caption your media file if applicable.')
    date_completed = forms.DateField(widget=forms.SelectDateWidget(), initial=get_default_localtime, required=False, help_text='When did you complete this workout?')

class ScheduleInstanceForm(forms.Form):
    date_to_be_added = forms.DateField(widget=forms.SelectDateWidget(), initial=get_default_localtime, help_text='When will you complete this workout?')
    repeat_yes = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    repeat_frequency = forms.ChoiceField(widget=forms.Select, choices=repetition_frequency_choices)
    number_of_repetitions = forms.IntegerField(widget=forms.NumberInput, required=False, help_text = 'XX number of times to repeat.')
    repeat_length = forms.ChoiceField(widget=forms.Select, choices=repetition_length_choices)

class EditScheduleForm(forms.Form):
    date_to_be_removed = forms.MultipleChoiceField(required=False, help_text='What date would you like to remove?')
    date_to_be_added = forms.DateField(required=False, widget=forms.SelectDateWidget(), initial=get_default_localtime, help_text='When will you complete this workout?')

class DeleteScheduleForm(forms.Form):
    date_to_be_removed = forms.MultipleChoiceField(help_text='What date would you like to remove?')

class HideInstanceForm(forms.Form):
    date_to_unhide = forms.DateField(required=False, widget=forms.SelectDateWidget(), initial=get_default_localtime, help_text='When would you like to unhide this workout?')
    
class EditInstanceForm(forms.Form):
    workout_text = forms.CharField(widget=forms.Textarea, max_length=2000, required=False)
    scaling_text= forms.CharField(widget=forms.Textarea, max_length=4000, required=False)
    duration_minutes = forms.IntegerField(required=False)
    duration_seconds = forms.IntegerField(required=False)

    def clean_duration_minutes(self):
        data = self.cleaned_data['duration_minutes']

        if data < 0:
            raise ValidationError(_('Invalid duration - duration cannot be negative'))
        return data

    def clean_duration_seconds(self):
        data = self.cleaned_data['duration_seconds']

        if data < 0:
            raise ValidationError(_('Invalid duration - duration cannot be negative'))
        return data

class EditStrengthInstanceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        super(EditStrengthInstanceForm, self).__init__(*args, **kwargs)
        if instance.strength_workout:
            for i in instance.strength_workout.strength_exercises.all():
                movement_name = 'movement_%s' % (i.strength_exercise_number,)
                self.fields[movement_name] = forms.ChoiceField(widget=forms.Select(), choices=movement_choices, required=False)
                self.fields[movement_name].initial = i.movement
                for q in i.set_set.all():
                    field_name = '%s_Set_%d_Reps' % (i.movement, q.set_number,)
                    self.fields[field_name] = forms.IntegerField(required=False, label = '%s, Set %d Reps' % (i.movement, q.set_number,))
                    self.fields[field_name].initial = q.reps
                    field_name = '%s_Set_%d_Weight' % (i.movement, q.set_number,)
                    self.fields[field_name] = forms.DecimalField(required=False, label = '%s, Set %d Weight' % (i.movement, q.set_number,))
                    self.fields[field_name].initial = q.weight
                field_name = 'comment_%s' % (i.strength_exercise_number,)
                self.fields[field_name] = forms.CharField(widget=forms.Textarea, max_length=4000, required=False)
                self.fields[field_name].initial = i.comment

class EditCardioInstanceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        super(EditCardioInstanceForm, self).__init__(*args, **kwargs)
        if instance.cardio_workout:
            for i in instance.cardio_workout.cardio_exercises.all():
                movement_name = 'movement_%s' % (i.cardio_exercise_number,)
                self.fields[movement_name] = forms.ChoiceField(widget=forms.Select(), choices=cardio_choices, required=False)
                self.fields[movement_name].initial = i.movement
                reps_field_name = movement_name + '_reps'
                self.fields[reps_field_name] = forms.IntegerField(required=False, label = 'Number of Reps')
                self.fields[reps_field_name].initial = i.number_of_reps
                distance_field_name = movement_name + '_distance'
                self.fields[distance_field_name] = forms.IntegerField(required=False, label = 'Distance/Time')
                self.fields[distance_field_name].initial = i.distance
                distance_units_field_name = movement_name + '_distance_units'
                self.fields[distance_units_field_name] = forms.ChoiceField(widget=forms.Select(), choices = distance_or_time_unit_choices, required=False, label = 'Distance Units')
                self.fields[distance_units_field_name].initial = i.distance_units
                rest_minutes_field_name = movement_name + '_rest_minutes'
                self.fields[rest_minutes_field_name] = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'rest_input'}), required=False, label='Rest (minutes)')
                self.fields[rest_minutes_field_name].initial = i.rest_in_minutes()
                rest_seconds_field_name = movement_name + '_rest_seconds'
                self.fields[rest_seconds_field_name] = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'rest_input'}), required=False, label='Rest (seconds)')
                self.fields[rest_seconds_field_name].initial = i.rest_remainder()
                pace_field_name = movement_name + '_pace'
                self.fields[pace_field_name] = forms.CharField(required=False, max_length=100, label='Pace')
                self.fields[pace_field_name].initial = i.pace
                field_name = 'comment_%s' % (i.cardio_exercise_number,)
                self.fields[field_name] = forms.CharField(widget=forms.Textarea, label = 'Comments', max_length=4000, required=False)
                self.fields[field_name].initial = i.comment
    
class EditGeneralResultForm(forms.Form):
    result_text = forms.CharField(widget=forms.Textarea, max_length=2000)
    duration_minutes = forms.IntegerField(required=False)
    duration_seconds = forms.IntegerField(required=False)
    date_completed = forms.DateField(widget=forms.SelectDateWidget(), required=False)

    def clean_duration_minutes(self):
        data = self.cleaned_data['duration_minutes']

        if data < 0:
            raise ValidationError(_('Invalid duration - duration cannot be negative'))
        return data

    def clean_duration_seconds(self):
        data = self.cleaned_data['duration_seconds']

        if data < 0:
            raise ValidationError(_('Invalid duration - duration cannot be negative'))
        return data
        
class EditStrengthResultForm(forms.Form):
    result_text = forms.CharField(widget=forms.Textarea, max_length=2000, required=False)
    date_completed = forms.DateField(widget=forms.SelectDateWidget(), required=False)
    
class EditCardioResultForm(forms.Form):
    result_text = forms.CharField(widget=forms.Textarea, max_length=2000, required=False)
    date_completed = forms.DateField(widget=forms.SelectDateWidget(), required=False)
