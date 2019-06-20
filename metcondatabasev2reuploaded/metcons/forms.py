from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from metcons.models import User

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

class AddCoachForm(forms.Form):
    coach_username = forms.CharField(max_length = 30, help_text='What is the coaches username? Lowercase letters only.')
    
class CreateWorkoutForm(forms.Form):
    workout_text = forms.CharField(widget=forms.Textarea, max_length=2000, help_text="Enter your workout")
    workout_scaling = forms.CharField(widget=forms.Textarea, max_length=4000, help_text='Enter any scaling options', required=False)
    estimated_duration = forms.IntegerField(help_text='Enter an estimate of how long it will take to complete the workout in minutes (whole numbers only)', required=False)
    gender = forms.ChoiceField(widget=forms.Select(), choices=workout_gender_choices, help_text='Is this workout (and the weights you have entered) applicable for both Males and Females or only one?')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CreateWorkoutForm, self).__init__(*args, **kwargs)
        if user.is_coach or user.is_gym_owner:
            self.fields['athlete_to_assign'] = forms.MultipleChoiceField(required=False, help_text='Which athletes would you like to assign this workout to? Default is yourself')
    
class CreateResultForm(forms.Form):
    result_text = forms.CharField(widget=forms.Textarea, max_length=2000, help_text="Enter your results here")
    duration_minutes = forms.IntegerField(required = False)
    duration_seconds = forms.IntegerField(required = False)
    media_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False, help_text='Attach any pictures or videos. Hold CTRL while selecting to upload multiple files.')
    media_file_caption = forms.CharField(required=False, help_text='Caption your media file if applicable')
    date_completed = forms.DateField(widget=forms.SelectDateWidget(), initial=get_default_localtime, required=False, help_text='When did you complete this workout?')

class ScheduleInstanceForm(forms.Form):
    date_to_be_added = forms.DateField(widget=forms.SelectDateWidget(), initial=get_default_localtime, help_text='When will you complete this workout?')
    repeat_yes = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    repeat_frequency = forms.ChoiceField(widget=forms.Select, choices=repetition_frequency_choices)
    number_of_repetitions = forms.IntegerField(widget=forms.NumberInput, required=False, help_text = 'XX number of times to repeat')
    repeat_length = forms.ChoiceField(widget=forms.Select, choices=repetition_length_choices)

class EditScheduleForm(forms.Form):
    date_to_be_removed = forms.MultipleChoiceField(help_text='What date would you like to remove?')
    date_to_be_added = forms.DateField(widget=forms.SelectDateWidget(), initial=get_default_localtime, help_text='When will you complete this workout?')

class DeleteScheduleForm(forms.Form):
    date_to_be_removed = forms.MultipleChoiceField(help_text='What date would you like to remove?')
    
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


class EditResultForm(forms.Form):
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
        
    
