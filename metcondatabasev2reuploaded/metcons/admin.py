from django.contrib import admin
from .models import Classification, Movement, Workout

admin.site.register(Classification)

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('display_name',
                    'estimated_duration_in_minutes',
                    'display_movement',
                    'classification',
                    'number_of_times_completed',
                    'date_created',
                    'display_classifications_of_movements')
    list_filter = ('estimated_duration_in_minutes', 'movements',
                   'classification')
    
@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    list_display = ('name', 'classification')
    list_filter = ['classification']