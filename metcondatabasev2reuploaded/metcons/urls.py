from django.urls import path
from . import views

urlpatterns = [
    path('profileredirect/', views.profileredirect),
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('workouts/', views.workoutlistview, name='workouts'),
    path('workout/<int:pk>', views.workoutdetailview, name='workout-detail'),
    path('movements/', views.MovementListView.as_view(), name='movements'),
    path('movement/<int:pk>', views.MovementDetailView.as_view(), name='movement-detail'),
    path('workout/create/', views.create_workout, name='workout_create'),
    path('movement/create/', views.MovementCreate.as_view(), name='movement_create'),
    path('<username>/workout/<int:pk>/addtoathletes/', views.add_workout_to_athletes, name='add_workout_to_athletes'),
    path('<username>/workout/<uuid:pk>/result/create/', views.create_result, name='result_create'),
    path('<username>/workout/<uuid:pk>/scheduleworkout/', views.schedule_instance, name='schedule_instance'),
    path('<username>/workout/<uuid:pk>/scheduleworkoutformultipleathletes/', views.schedule_instance_for_multiple_athletes, name='schedule_instance_for_multiple_athletes'),
    path('<username>/workout/<uuid:pk>/editschedule/', views.edit_schedule, name='edit_schedule'),
    path('<username>/workout/<uuid:pk>/editscheduleformultipleathletes/', views.edit_schedule_for_multiple_athletes, name='edit_schedule_for_multiple_athletes'),
    path('<username>/workout/<uuid:pk>/deleteschedule/', views.delete_schedule, name='delete_schedule'),
    path('<username>/', views.profile, name='profile'),
    path('<username>/workout/<uuid:pk>/', views.workoutinstancedetailview, name='workoutinstance-detail'),
    path('<username>/workout/<uuid:pk>/hideinstance', views.hide_instance, name='hide_instance'),
    path('<username>/workout/<uuid:pk>/edit/', views.edit_instance, name='edit_instance'),
    path('<username>/workout/<uuid:pk>/delete/', views.delete_instance, name='delete_instance'),
    path('<username>/workout/<uuid:pk>/result/<int:resultid>/edit/', views.edit_result, name='edit_result'),
    path('<username>/workout/<uuid:pk>/result/<int:resultid>/delete/', views.delete_result, name='delete_result'),
    path('<username>/workout/<uuid:pk>/scheduleoraddresult/', views.interim_created_workout, name='interim_created_workout'),
    path('<username>/workout/<uuid:pk>/schedulerecentlycreatedworkoutformultipleathletes/', views.interim_created_workout_for_multiple_athletes, name='interim_created_workout_for_multiple_athletes'),
    path('<username>/addathlete/', views.add_athletes_to_coach, name='add_athletes'),
##    path('<username>/removeathletes/', views.remove_athletes_from_coach, name='remove_athletes_from_coach'),
    path('<username>/addcoach/', views.add_coach, name='add_coach'),
##    path('<username>/removecoach/', views.remove_coaches_from_athlete, name='remove_coaches_from_athlete'),
    path('<username>/remove/', views.remove_coach_or_athlete, name='remove_coach_or_athlete'),
##    path('<username>/requests/', views.request_list_view, name='request_list'),
    path('<username>/requests/<int:pk>/', views.request_detail, name='request_detail'),
    path('<username>/group/create/', views.create_group, name='create_group'),
    path('<username>/group/<int:pk>/delete/', views.delete_group, name='delete_group'),
    path('<username>/group/<int:pk>/', views.group_detail, name='group_detail'),
    path('<username>/group/<int:pk>/addathletestogroup/', views.add_athletes_to_group, name='add_athletes_to_group'),
    path('<username>/group/<int:pk>/removeathletesfromgroup/', views.remove_athletes_from_group, name='remove_athletes_from_group'),
]
