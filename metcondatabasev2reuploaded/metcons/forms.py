from django import forms
from django.utils import timezone

class CreateWorkoutForm(forms.Form):
    workout_text = forms.CharField(widget=forms.Textarea, help_text="Enter your workout")
    workout_scaling = forms.CharField(widget=forms.Textarea, help_text='Enter any scaling options', required=False)
    estimated_duration = forms.IntegerField(help_text='Enter an estimate of how long it will take to complete the workout in minutes (whole numbers only)', required=False)
    what_website_workout_came_from = forms.CharField(max_length=200, required=False)

    #can likely delete all these clean statements as calling form.is_valid() from the view cleans all data and passes to cleaned_data attribute
    def clean_workout_text(self):
        return self.cleaned_data['workout_text']
        
    def clean_workout_scaling(self):
        return self.cleaned_data['workout_scaling']

    def clean_estimated_duration(self):
        return self.cleaned_data['estimated_duration']

    def clean_what_website_workout_came_from(self):
        return self.cleaned_data['what_website_workout_came_from']

class CreateResultForm(forms.Form):
    result_text = forms.CharField(widget=forms.Textarea, help_text="Enter your results here")
    duration_minutes = forms.IntegerField(initial=0, required = False)
    duration_seconds = forms.IntegerField(initial=0, required = False)
    media_file = forms.FileField(required=False, help_text='Attach any pictures or videos')
    media_file_caption = forms.CharField(required=False, help_text='Caption your media file if applicable')
    date_completed = forms.DateField(widget=forms.SelectDateWidget(), initial=timezone.now, required=False, help_text='When did you complete this workout?')

class ScheduleInstanceForm(forms.Form):
    date_to_be_completed1 = forms.DateField(widget=forms.SelectDateWidget(), initial=timezone.now, help_text='When will you complete this workout?')
