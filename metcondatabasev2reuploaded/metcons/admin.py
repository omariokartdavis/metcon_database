from django.contrib import admin
from .models import Classification, Movement, Workout, WorkoutInstance, WorkoutInstanceCompletedDate

admin.site.register(Classification)

class WorkoutInstanceInline(admin.TabularInline):
    model = WorkoutInstance
    extra = 0
    
@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('display_name',
                    'created_by_user',
                    'estimated_duration_in_minutes',
                    'display_movement',
                    'classification',
                    'number_of_times_completed',
                    'number_of_instances',
                    'date_created',
                    'display_classifications_of_movements')
    list_filter = ('classification',
                   'estimated_duration_in_minutes',
                   'movements',
                   )
    inlines = [WorkoutInstanceInline]
    
@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    list_display = ('name', 'classification')
    list_filter = ['classification']


    
@admin.register(WorkoutInstance)
class WorkoutInstance(admin.ModelAdmin):
    list_display = ('display_name',
                    'current_user',
                    'display_dates_completed',
                    'date_added_by_user',
                    'id',
                    'number_of_times_completed',
                    'duration_in_minutes',
                    )

                    
admin.site.register(WorkoutInstanceCompletedDate)
    
