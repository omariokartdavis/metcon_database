from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

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

def get_default_localtime():
    return timezone.localtime(timezone.now())

class CreateWorkoutForm(forms.Form):
    workout_text = forms.CharField(widget=forms.Textarea, max_length=2000, help_text="Enter your workout")
    workout_scaling = forms.CharField(widget=forms.Textarea, max_length=4000, help_text='Enter any scaling options', required=False)
    estimated_duration = forms.IntegerField(help_text='Enter an estimate of how long it will take to complete the workout in minutes (whole numbers only)', required=False)

class CreateResultForm(forms.Form):
    result_text = forms.CharField(widget=forms.Textarea, max_length=2000, help_text="Enter your results here")
    duration_minutes = forms.IntegerField(required = False)
    duration_seconds = forms.IntegerField(required = False)
    media_file = forms.FileField(required=False, help_text='Attach any pictures or videos')
    media_file_caption = forms.CharField(required=False, help_text='Caption your media file if applicable')
    date_completed = forms.DateField(widget=forms.SelectDateWidget(), initial=get_default_localtime, required=False, help_text='When did you complete this workout?')

class ScheduleInstanceForm(forms.Form):
    date_to_be_completed = forms.DateField(widget=forms.SelectDateWidget(), initial=get_default_localtime, help_text='When will you complete this workout?')
    repeat_yes = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    repeat_frequency = forms.ChoiceField(widget=forms.Select, choices=repetition_frequency_choices)
    number_of_repetitions = forms.IntegerField(widget=forms.NumberInput, required=False, help_text = 'XX number of times to repeat')
    repeat_length = forms.ChoiceField(widget=forms.Select, choices=repetition_length_choices)

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
        
    
