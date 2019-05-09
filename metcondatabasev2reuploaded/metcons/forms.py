from django import forms

class CreateWorkoutForm(forms.Form):
    workout_text = forms.CharField(widget=forms.Textarea, help_text="Enter your workout")
    workout_scaling = forms.CharField(widget=forms.Textarea, help_text='Enter any scaling options', required=False)
    estimated_duration = forms.IntegerField(help_text='Enter how long it will take to complete the workout', required=False)
    what_website_workout_came_from = forms.CharField(max_length=200, required=False)

    def clean_workout_text(self):
        return self.cleaned_data['workout_text']
        
    def clean_workout_scaling(self):
        return self.cleaned_data['workout_scaling']

    def clean_estimated_duration(self):
        return self.cleaned_data['estimated_duration']

    def clean_what_website_workout_came_from(self):
        return self.cleaned_data['what_website_workout_came_from']
