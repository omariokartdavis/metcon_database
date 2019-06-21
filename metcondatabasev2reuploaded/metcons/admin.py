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
    
@admin.register(User)
class UserProfileAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {
            'fields': ('user_gender', 'workout_default_gender')
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
    
