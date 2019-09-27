from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

class WorkoutInstanceInline(admin.TabularInline):
    model = WorkoutInstance
    extra = 0

    fields = ['display_workout', 'number_of_times_completed', 'duration_in_seconds',
              'youngest_scheduled_date', 'oldest_completed_date',
              'edited_workout_text',
              ]
    readonly_fields = ['display_workout']

class SetInline(admin.TabularInline):
    model = Set
    extra = 0

    fields = ['display_name', 'set_number', 'reps', 'weight', 'weight_units']

    readonly_fields = ['display_name']
    
@admin.register(User)
class UserProfileAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {
            'fields': ('user_gender', 'workout_default_gender', 'strength_program')
            }),
        ('Athlete Status', {
            'fields': ('is_athlete', 'is_coach', 'is_gym_owner')
            }),
        ('Privacy', {
            'fields': ('user_profile_privacy', 'workout_default_privacy')
            }),
        )

##    inlines = [WorkoutInstanceInline] very slow and expensive with a lot of instances

admin.site.register(Classification)

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('requestor',
                    'requestee',
                    'date_requested',
                    'is_adding_athlete',
                    'is_adding_coach',
                    'is_adding_gymowner',
                    )
    
@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    list_display = ('user',
                    'gym_owner',
                    )

@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ('user',
                    )

@admin.register(GymOwner)
class GymOwnerAdmin(admin.ModelAdmin):
    list_display = ('user',
                    )

@admin.register(Group)
class GroupAdmin (admin.ModelAdmin):
    list_display = ('name',
                    'coach',
                    )                    
    
@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('display_name',
                    'created_by_user',
                    'where_workout_came_from',
                    'estimated_duration_in_seconds',
##                    'display_movement', removed for expensiveness of operation
                    'classification',
                    'number_of_times_completed',
                    'number_of_instances',
                    'date_created',
                    'date_added_to_database')
    list_filter = ('classification',
                   'estimated_duration_in_seconds',
                   'movements',
                   'created_by_user',
                   )
    inlines = [WorkoutInstanceInline]

@admin.register(StrengthWorkout)
class StrengthWorkoutAdmin(admin.ModelAdmin):
    list_display = ('display_name',
                    'created_by_user',
                    'number_of_times_completed',
                    'date_created',
                    'date_added_to_database')

@admin.register(StrengthExercise)
class StrengthExerciseAdmin(admin.ModelAdmin):
    list_display = ('display_name',
                    'date_created',
                    'movement',
                    'number_of_sets',
                    'strength_exercise_number')
    inlines = [SetInline]

@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    list_display = ('display_name',
                    'set_number',
                    'reps',
                    'weight',
                    'weight_units')

@admin.register(StrengthProgram)
class StrengthProgramAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'weight_increase_timeline')
    
@admin.register(StrengthProgramInstance)
class StrengthProgramInstanceAdmin(admin.ModelAdmin):
    list_display = ('day_variation',
                    'display_strength_program')
    
@admin.register(CardioWorkout)
class CardioWorkoutAdmin(admin.ModelAdmin):
    list_display = ('display_name',
                    'created_by_user',
                    'number_of_times_completed',
                    'date_created',
                    'date_added_to_database')

@admin.register(CardioExercise)
class CardioExerciseAdmin(admin.ModelAdmin):
    list_display = ('display_name',
                    'movement',
                    'distance',
                    'distance_units',
                    'number_of_reps',
                    'pace',
                    'rest',
                    'cardio_exercise_number')
    
@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    list_display = ('name', 'classification')
    list_filter = ['classification']


class ResultInline(admin.TabularInline):
    model = Result
    extra = 0

    fields = ['display_result', 'date_workout_completed', 'result_text', 'duration_in_seconds']
    readonly_fields = ['display_result']
    show_change_link = True
    
@admin.register(WorkoutInstance)
class WorkoutInstanceAdmin(admin.ModelAdmin):
    list_display = ('display_workout',
                    'current_user',
                    'oldest_completed_date',
                    'youngest_scheduled_date',
                    'date_added_by_user',
                    'id',
                    'number_of_times_completed',
                    'duration_in_seconds',
                    'is_from_strength_program'
                    )
    inlines = [ResultInline]
    list_filter = ['current_user']
    
class ResultFileInline(admin.TabularInline):
    model = ResultFile
    extra = 0

    fields = ['display_resultfile', 'file', 'caption', 'content_type']
    readonly_fields = ['display_resultfile']
    show_change_link = True
    
@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('display_result',
                    'date_created',
                    'date_workout_completed',
                    'workoutinstance',
                    )
    inlines = [ResultFileInline]
    
@admin.register(ResultFile)
class ResultFileAdmin(admin.ModelAdmin):
    list_display = ('display_resultfile',
                    'date_created',
                    'result',
                    'caption',
                    'display_workout',
                    )
    
admin.site.register(Date)
    
