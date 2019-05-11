from django.db import models
from django.urls import reverse
import datetime
import uuid
from django.conf import settings
from django.db.models import Count

class Classification(models.Model):
        """Model representing a classification of a movement"""
        classification_types = (
            ('Upper Body', 'Upper Body'),
            ('Lower Body', 'Lower Body'),
            ('Total Body', 'Total Body'),
            ('Cardio', 'Cardio'),
            )
        
        name = models.CharField(max_length=20,
                                choices = classification_types,
                                null=True,
                                blank=True,
                                default='Total Body',
                                help_text='Is this movement upper, lower, total body or cardio?'
                                )

        def __str__(self):
            if self.name:
                return self.name

class Movement(models.Model):
	"""Model representing a movement type in a workout"""
	name = models.CharField(max_length=200)
	classification = models.ForeignKey(Classification, default=3, on_delete=models.CASCADE)
	
	class Meta:
		ordering = ['name']
		
	def __str__(self):
		"""String for representing the model object."""
		return self.name

	def get_absolute_url(self):
                """Returns the url to access a detail record for this workout."""
                return reverse('movement-detail', args=[str(self.id)])
	
class Workout(models.Model):
        """Model representing a workout."""
        #when creating a model from the admin page, the model will not set the classifications/movements itself.
        #each workout needs an instance model in order to track number of times completed for each user
        date_created = models.DateField(default=datetime.date.today)
        date_added_to_database = models.DateField(auto_now_add = True)
        number_of_times_completed = models.IntegerField(default=0)
        workout_text = models.TextField(max_length=2000)
        scaling_or_description_text = models.TextField(max_length=4000, null=True, blank=True)
        what_website_workout_came_from = models.CharField(max_length=200, null=True, blank=True)
        estimated_duration_in_minutes = models.IntegerField(default=0, null=True, blank=True)
        created_by_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
                
        movements = models.ManyToManyField(Movement, blank=True)

        classification = models.ForeignKey(Classification, default=3, blank=True, null=True, on_delete=models.CASCADE)

        
        #Required for running both functions on click in html
        #next step is to transfer this to javascript so you can also force page reload at the same time
        def update_movements_and_classification(self):
                self.update_movements()
                self.update_classification()
                self.save()
                
        #This is called from the create workout form.
        def update_movements(self):
                for i in Movement.objects.all():
                        if i.name.lower() in self.workout_text.lower():
                                self.movements.add(i)
        
        #This is called from the create workout form.
        def update_classification(self):                 
            movement_classifications = []
            for movement in self.movements.all():
                movement_classifications.append(movement.classification.name)
            if 'Total Body' in movement_classifications:
                self.classification = Classification.objects.get(name='Total Body') 
            elif 'Upper Body' in movement_classifications:
                if 'Lower Body' in movement_classifications:
                    self.classification = Classification.objects.get(name='Total Body')
                else:
                    self.classification = Classification.objects.get(name='Upper Body')
            elif 'Lower Body' in movement_classifications:
                self.classification = Classification.objects.get(name='Lower Body')
            elif 'Cardio' in movement_classifications:
                self.classification = Classification.objects.get(name='Cardio')
            elif 'Core' in movement_classifications:
                self.classification = Classification.objects.get(name='Core')
            else:
                self.classification = None

        def increment_times_completed_counter(self):
                #not sure if this is the proper way to do this
                self.number_of_times_completed += 1
                self.save()
            
        def number_of_instances(self):
                count = WorkoutInstance.objects.filter(workout__id = self.id).count()
                return count
        
        class Meta:
                ordering = ['-number_of_times_completed', '-date_created', '-id']

        def display_name(self):
                name = "Workout " + str(self.id)
                return name

        display_name.short_description = 'Name'

        def display_movement(self):
                """Create a string for the movement. required to display movements in admin site"""
                return ', '.join(movement.name for movement in self.movements.all()[:3])

        display_movement.short_description = 'Movement'

        def display_classifications_of_movements(self):
                """Create a string for the classification. required to display classificaitons in admin site"""
                return ', '.join(movement.classification.name for movement in self.movements.all()[:3])

        display_classifications_of_movements.short_description = 'Classification of Individual Movements'

        def get_absolute_url(self):
                """Returns the url to access a detail record for this workout."""
                return reverse('workout-detail', args=[str(self.id)])

        def __str__(self):
                """String for representing the model object."""
                name = "Workout " + str(self.id)
                return name
        
class WorkoutInstanceCompletedDate(models.Model):
        """Dates of when workout instances are completed"""
        date_completed = models.DateField(default=datetime.date.today)

        class Meta:
                ordering = ['-date_completed']

        def __str__(self):
                name = str(self.date_completed)
                return name
        
class WorkoutInstance(models.Model):
        """Model representing a specific Users Workout Instance"""
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text = 'Unique ID for this particular workout')
        dates_workout_completed = models.ManyToManyField(WorkoutInstanceCompletedDate, blank=True)
        date_added_by_user = models.DateField(auto_now_add=True)
        workout = models.ForeignKey(Workout, on_delete=models.SET_NULL, null=True)
        number_of_times_completed = models.IntegerField(default=0)
        duration_in_minutes = models.IntegerField(default=0, null=True, blank=True)
        current_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

        current_user.short_description = 'User'
        
        class Meta:
                ordering = ['-number_of_times_completed', '-date_added_by_user', '-id']
                
        def add_date_completed(self, date):
                #need to work on this as not currently sure what type I want date input to be. should it be a string or datetime object? datetime object likely easier but how do I get it into
                # that form?
                all_current_dates = WorkoutInstanceCompletedDate.objects.all()
                if date in all_current_dates:
                        self.dates_workout_completed.add(date)
                else:
                        new_date = WorkoutInstanceCompletedDate(date_completed = date)
                        self.dates_workout_completed.add(new_date)
                        
        def increment_times_completed(self):
                #not sure if this works or is proper
                self.number_of_times_completed += 1
                self.save()
                self.workout.increment_times_completed_counter()
                
        def display_name(self):
                name = self.workout.display_name()
                return name

        def display_dates_completed(self):
                """Create a string for the classification. required to display classificaitons in admin site"""
                return ', '.join(str(date) for date in self.dates_workout_completed.all()[:3])

        display_dates_completed.short_description = 'Dates Completed'
        
        def __str__(self):
                name = self.workout.display_name()
                return name
