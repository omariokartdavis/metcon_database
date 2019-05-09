from django.db import models
from django.urls import reverse
import datetime

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

	classifications = models.ForeignKey(Classification, default=3, on_delete=models.CASCADE)
	
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
        date_completed = models.DateField(auto_now=True)
        number_of_times_completed = models.IntegerField(default=0)
        workout_text = models.TextField(max_length=2000)
        scaling_or_description_text = models.TextField(max_length=4000, null=True, blank=True)
        what_website_workout_came_from = models.CharField(max_length=200, null=True, blank=True)
        estimated_duration_in_minutes = models.IntegerField(default=0, null=True, blank=True)
                
        movements = models.ManyToManyField(Movement, blank=True)

        classifications = models.ForeignKey(Classification, default=3, blank=True, null=True, on_delete=models.CASCADE) #had to run makemigrations and migrate after making the blank=true null=True change to allow for no classifications when creating a workout model

        #Required for running both functions on click in html
        #next step is to transfer this to javascript so you can also force page reload at the same time
        def update_movements_and_classification(self):
                #self.update_classification()
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
                movement_classifications.append(movement.classifications.name)
            if 'Total Body' in movement_classifications:
                self.classifications = Classification.objects.get(name='Total Body') 
            elif 'Upper Body' in movement_classifications:
                if 'Lower Body' in movement_classifications:
                    self.classifications = Classification.objects.get(name='Total Body')
                else:
                    self.classifications = Classification.objects.get(name='Upper Body')
            elif 'Lower Body' in movement_classifications:
                self.classifications = Classification.objects.get(name='Lower Body')
            elif 'Cardio' in movement_classifications:
                self.classifications = Classification.objects.get(name='Cardio')
            else:
                self.classifications = None

        def update_times_completed_counter(self):
                self.number_of_times_completed += 1
            
            
        class Meta:
                ordering = [ '-date_created', '-number_of_times_completed', '-id']

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
                return ', '.join(movement.classifications.name for movement in self.movements.all()[:3])

        display_classifications_of_movements.short_description = 'Classification of Individual Movements'

        def get_absolute_url(self):
                """Returns the url to access a detail record for this workout."""
                return reverse('workout-detail', args=[str(self.id)])

        def __str__(self):
                """String for representing the model object."""
                name = "Workout " + str(self.id)
                return name
