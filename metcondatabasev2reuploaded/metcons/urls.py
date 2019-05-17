from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('workouts/', views.workoutlistview, name='workouts'),
    path('workout/<int:pk>', views.workoutdetailview, name='workout-detail'),
    path('movements/', views.MovementListView.as_view(), name='movements'),
    path('movement/<int:pk>', views.MovementDetailView.as_view(), name='movement-detail'),
    path('workout/create/', views.create_workout, name='workout_create'),
    path('movement/create/', views.MovementCreate.as_view(), name='movement_create'),
    path('<username>/', views.profile, name='profile'),
    path('<username>/workout/<uuid:pk>', views.WorkoutInstanceDetailView.as_view(), name='workoutinstance-detail'),
]
