from django.contrib import admin
from .models import Classification, Movement, Workout, WorkoutInstance, Date, Result, ResultFile, User
from django.contrib.auth.admin import UserAdmin

#admin.site.register(User, UserAdmin)
@admin.register(User)
class UserProfileAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('gender',)}),
        )

admin.site.register(Classification)

class WorkoutInstanceInline(admin.TabularInline):
    model = WorkoutInstance
    extra = 0
    
@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('display_name',
                    'created_by_user',
                    'where_workout_came_from',
                    'estimated_duration_in_seconds',
                    'display_movement',
                    'classification',
                    'number_of_times_completed',
                    'number_of_instances',
                    'date_created',
                    'date_added_to_database')
    list_filter = ('classification',
                   'estimated_duration_in_seconds',
                   'movements',
                   )
    inlines = [WorkoutInstanceInline]
    
@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    list_display = ('name', 'classification')
    list_filter = ['classification']


class ResultInline(admin.TabularInline):
    model = Result
    extra = 0
    
@admin.register(WorkoutInstance)
class WorkoutInstanceAdmin(admin.ModelAdmin):
    list_display = ('display_workout',
                    'current_user',
                    'display_dates_completed',
                    'display_dates_scheduled',
                    'date_added_by_user',
                    'id',
                    'number_of_times_completed',
                    'duration_in_seconds',
                    )
    inlines = [ResultInline]
    
class ResultFileInline(admin.TabularInline):
    model = ResultFile
    extra = 0
    
@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('date_created',
                    'date_workout_completed',
                    'workoutinstance',
                    )
    inlines = [ResultFileInline]
    
@admin.register(ResultFile)
class ResultFileAdmin(admin.ModelAdmin):
    list_display = ('date_created',
                    'result',
                    'caption',
                    'display_workout',
                    )
    
admin.site.register(Date)
    
