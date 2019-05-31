from django.urls import path
from . import views

urlpatterns = [
    path('profileredirect/', views.profileredirect),
    path('', views.index, name='index'),
    path('workouts/', views.workoutlistview, name='workouts'),
    path('workout/<int:pk>', views.workoutdetailview, name='workout-detail'),
    path('movements/', views.MovementListView.as_view(), name='movements'),
    path('movement/<int:pk>', views.MovementDetailView.as_view(), name='movement-detail'),
    path('workout/create/', views.create_workout, name='workout_create'),
    path('movement/create/', views.MovementCreate.as_view(), name='movement_create'),
    path('<username>/workout/<uuid:pk>/result/create/', views.create_result, name='result_create'),
    path('<username>/workout/<uuid:pk>/scheduleworkout/', views.schedule_instance, name='schedule_instance'),
    path('<username>/workout/<uuid:pk>/editschedule/', views.edit_schedule, name='edit_schedule'),
    path('<username>/', views.profile, name='profile'),
    path('<username>/workout/<uuid:pk>', views.WorkoutInstanceDetailView.as_view(), name='workoutinstance-detail'),
    path('<username>/workout/<uuid:pk>/edit', views.edit_instance, name='edit_instance'),
    path('<username>/workout/<uuid:pk>/delete', views.delete_instance, name='delete_instance'),
    path('<username>/workout/<uuid:pk>/result/<int:resultid>/edit', views.edit_result, name='edit_result'),
    path('<username>/workout/<uuid:pk>/result/<int:resultid>/delete', views.delete_result, name='delete_result'),
]
