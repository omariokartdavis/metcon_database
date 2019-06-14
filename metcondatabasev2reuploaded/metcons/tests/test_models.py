from django.test import TestCase
from metcons.models import User, Classification, Movement, Workout, Date, WorkoutInstance, Result, ResultFile
from django.utils import timezone

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        User.objects.create(username='odavis', password='4a0308ki9ps', gender='M')

    def test_gender_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('gender').verbose_name
        self.assertEquals(field_label, 'gender')

    def test_gender_max_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field('gender').max_length
        self.assertEquals(max_length, 1)

class ClassificationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        Classification.objects.create(name='Upper Body')

    def test_name_label(self):
        classification = Classification.objects.get(id=1)
        field_label = classification._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_name_max_length(self):
        classification = Classification.objects.get(id=1)
        max_length = Classification._meta.get_field('name').max_length
        self.assertEquals(max_length, 20)

    def test_object_name_is_name(self):
        classification = Classification.objects.get(id=1)
        expected_object_name = f'{classification.name}'
        self.assertEquals(expected_object_name, str(classification))

class MovementModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Classification.objects.create(name='Upper Body')
        upper_body = Classification.objects.get(id=1)
        Movement.objects.create(name='Pull Up', classification=upper_body)

    def test_name_label(self):
        movement = Movement.objects.get(id=1)
        field_label = movement._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_classification_label(self):
        movement = Movement.objects.get(id=1)
        field_label = movement._meta.get_field('classification').verbose_name
        self.assertEquals(field_label, 'classification')

    def test_name_max_length(self):
        movement = Movement.objects.get(id=1)
        max_length = Movement._meta.get_field('name').max_length
        self.assertEquals(max_length, 200)

    def test_object_name_is_name(self):
        movement = Movement.objects.get(id=1)
        expected_object_name = f'{movement.name}'
        self.assertEquals(expected_object_name, str(movement))

    def test_get_absolute_url(self):
        movement = Movement.objects.get(id=1)
        self.assertEquals(movement.get_absolute_url(), '/metcons/movement/1')

class WorkoutModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='odavis', password='4a0308ki9ps', gender='M')
        user = User.objects.get(id=1)
        Classification.objects.create(name='Upper Body')
        upper_body = Classification.objects.get(id=1)
        Movement.objects.create(name='Pull Up', classification=upper_body)
        Workout.objects.create(workout_text='Pull Up', created_by_user=user)
        workout = Workout.objects.get(id=1)
        WorkoutInstance.objects.create(workout=workout, current_user=user, duration_in_seconds = 600)
        instance = WorkoutInstance.objects.get(workout=workout, current_user=user)

    def test_date_created_label(self):
        workout = Workout.objects.get(id=1)
        field_label = workout._meta.get_field('date_created').verbose_name
        self.assertEquals(field_label, 'date created')

    def test_date_added_to_database_label(self):
        workout = Workout.objects.get(id=1)
        field_label = workout._meta.get_field('date_added_to_database').verbose_name
        self.assertEquals(field_label, 'date added to database')

    def test_number_of_times_completed_label(self):
        workout = Workout.objects.get(id=1)
        field_label = workout._meta.get_field('number_of_times_completed').verbose_name
        self.assertEquals(field_label, 'Times Completed')

    def test_workout_text_label(self):
        workout = Workout.objects.get(id=1)
        field_label = workout._meta.get_field('workout_text').verbose_name
        self.assertEquals(field_label, 'workout text')

    def test_scaling_or_description_text_label(self):
        workout = Workout.objects.get(id=1)
        field_label = workout._meta.get_field('scaling_or_description_text').verbose_name
        self.assertEquals(field_label, 'scaling or description text')

    def test_where_workout_came_from_label(self):
        workout = Workout.objects.get(id=1)
        field_label = workout._meta.get_field('where_workout_came_from').verbose_name
        self.assertEquals(field_label, 'where workout came from')

    def test_estimated_duration_in_seconds_label(self):
        workout = Workout.objects.get(id=1)
        field_label = workout._meta.get_field('estimated_duration_in_seconds').verbose_name
        self.assertEquals(field_label, 'Duration (sec)')

    def test_created_by_user_label(self):
        workout = Workout.objects.get(id=1)
        field_label = workout._meta.get_field('created_by_user').verbose_name
        self.assertEquals(field_label, 'created by user')

    def test_gender_label(self):
        workout = Workout.objects.get(id=1)
        field_label = workout._meta.get_field('gender').verbose_name
        self.assertEquals(field_label, 'gender')

    def test_movements_label(self):
        workout = Workout.objects.get(id=1)
        field_label = workout._meta.get_field('movements').verbose_name
        self.assertEquals(field_label, 'movements')

    def test_classification_label(self):
        workout = Workout.objects.get(id=1)
        field_label = workout._meta.get_field('classification').verbose_name
        self.assertEquals(field_label, 'classification')

    def test_workout_text_max_length(self):
        workout = Workout.objects.get(id=1)
        max_length = Workout._meta.get_field('workout_text').max_length
        self.assertEquals(max_length, 2000)

    def test_scaling_or_description_text_max_length(self):
        workout = Workout.objects.get(id=1)
        max_length = Workout._meta.get_field('scaling_or_description_text').max_length
        self.assertEquals(max_length, 4000)

    def test_where_workout_came_from_max_length(self):
        workout = Workout.objects.get(id=1)
        max_length = Workout._meta.get_field('where_workout_came_from').max_length
        self.assertEquals(max_length, 200)

    def test_gender_max_length(self):
        workout = Workout.objects.get(id=1)
        max_length = Workout._meta.get_field('gender').max_length
        self.assertEquals(max_length, 1)

    def test_object_name_is_workout_id(self):
        workout = Workout.objects.get(id=1)
        expected_object_name = f'Workout {workout.id}'
        self.assertEquals(expected_object_name, str(workout))

    def test_get_absolute_url(self):
        workout = Workout.objects.get(id=1)
        self.assertEquals(workout.get_absolute_url(), '/metcons/workout/1')

    def test_update_movements(self):
        workout = Workout.objects.get(id=1)
        workout.update_movements()
        name_of_movement = ''
        for i in workout.movements.all():
            name_of_movement = i.name
        self.assertEquals(name_of_movement, 'Pull Up')

    def test_update_classification(self):
        workout = Workout.objects.get(id=1)
        workout.update_movements()
        workout.update_classification()
        expected_classification_name = 'Upper Body'
        self.assertEquals(expected_classification_name, workout.classification.name)

    def test_update_movements_and_classification(self):
        workout = Workout.objects.get(id=1)
        workout.update_movements_and_classification()
        name_of_movement = ''
        for i in workout.movements.all():
            name_of_movement = i.name
        expected_classification_name = 'Upper Body'
        self.assertEquals(name_of_movement, 'Pull Up')
        self.assertEquals(expected_classification_name, workout.classification.name)

    def test_update_estimated_duration(self):
        workout=Workout.objects.get(id=1)
        workout.update_estimated_duration()
        self.assertEquals(workout.estimated_duration_in_seconds, 600)

    def test_update_times_completed(self):
        workout = Workout.objects.get(id=1)
        instance = WorkoutInstance.objects.get(workout=workout)
        instance.number_of_times_completed=1
        instance.save()
        workout.update_times_completed()
        self.assertEquals(workout.number_of_times_completed, 1)
        
    def test_number_of_instances(self):
        workout = Workout.objects.get(id=1)
        self.assertEquals(workout.number_of_instances(), 1)

    def test_display_name_is_workout_id(self):
        workout = Workout.objects.get(id=1)
        expected_object_name = f'Workout {workout.id}'
        self.assertEquals(workout.display_name(), expected_object_name)

    def test_display_movement(self):
        workout = Workout.objects.get(id=1)
        pull_up = Movement.objects.get(id=1)
        workout.movements.add(pull_up)
        self.assertEquals(workout.display_movement(), 'Pull Up')

    def test_classifications_of_movenets(self):
        workout = Workout.objects.get(id=1)
        pull_up = Movement.objects.get(id=1)
        workout.movements.add(pull_up)
        self.assertEquals(workout.display_classifications_of_movements(), 'Upper Body')

class DateModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Date.objects.create()

    def test_date_completed_label(self):
        date = Date.objects.get(id=1)
        field_label = date._meta.get_field('date_completed').verbose_name
        self.assertEquals(field_label, 'date completed')

    def test_object_name_is_date_completed(self):
        date = Date.objects.get(id=1)
        expected_object_name = f'{date.date_completed}'
        self.assertEquals(expected_object_name, str(date))

class WorkoutInstanceModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='odavis', password='4a0308ki9ps', gender='M')
        user = User.objects.get(id=1)
        Classification.objects.create(name='Upper Body')
        upper_body = Classification.objects.get(id=1)
        Movement.objects.create(name='Pull Up', classification=upper_body)
        Workout.objects.create(workout_text='Pull Up', created_by_user=user)
        workout = Workout.objects.get(id=1)
        WorkoutInstance.objects.create(workout=workout, current_user=user, duration_in_seconds = 600)
        instance = WorkoutInstance.objects.get(workout=workout, current_user=user)
        Result.objects.create(workoutinstance=instance)

    def test_id_label(self):
        workout = Workout.objects.get(id=1)
        instance = WorkoutInstance.objects.get(workout=workout)
        field_label = instance._meta.get_field('id').verbose_name
        self.assertEquals(field_label, 'id')

    def test_dates_workout_completed_label(self):
        workout = Workout.objects.get(id=1)
        instance = WorkoutInstance.objects.get(workout=workout)
        field_label = instance._meta.get_field('dates_workout_completed').verbose_name
        self.assertEquals(field_label, 'dates workout completed')
        
    def test_dates_to_be_completed_label(self):
        workout = Workout.objects.get(id=1)
        instance = WorkoutInstance.objects.get(workout=workout)
        field_label = instance._meta.get_field('dates_to_be_completed').verbose_name
        self.assertEquals(field_label, 'dates to be completed')

    def test_date_added_by_user_label(self):
        workout = Workout.objects.get(id=1)
        instance = WorkoutInstance.objects.get(workout=workout)
        field_label = instance._meta.get_field('date_added_by_user').verbose_name
        self.assertEquals(field_label, 'date added by user')

    def test_workout_label(self):
        workout = Workout.objects.get(id=1)
        instance = WorkoutInstance.objects.get(workout=workout)
        field_label = instance._meta.get_field('workout').verbose_name
        self.assertEquals(field_label, 'workout')

    def test_number_of_times_completed_label(self):
        workout = Workout.objects.get(id=1)
        instance = WorkoutInstance.objects.get(workout=workout)
        field_label = instance._meta.get_field('number_of_times_completed').verbose_name
        self.assertEquals(field_label, 'Times Completed')

    def test_duration_in_seconds_label(self):
        workout = Workout.objects.get(id=1)
        instance = WorkoutInstance.objects.get(workout=workout)
        field_label = instance._meta.get_field('duration_in_seconds').verbose_name
        self.assertEquals(field_label, 'Duration (sec)')

    def test_current_user_label(self):
        workout = Workout.objects.get(id=1)
        instance = WorkoutInstance.objects.get(workout=workout)
        field_label = instance._meta.get_field('current_user').verbose_name
        self.assertEquals(field_label, 'User')

    def test_youngest_scheduled_date_label(self):
        workout = Workout.objects.get(id=1)
        instance = WorkoutInstance.objects.get(workout=workout)
        field_label = instance._meta.get_field('youngest_scheduled_date').verbose_name
        self.assertEquals(field_label, 'youngest scheduled date')

    def test_oldest_completed_date_label(self):
        workout = Workout.objects.get(id=1)
        instance = WorkoutInstance.objects.get(workout=workout)
        field_label = instance._meta.get_field('oldest_completed_date').verbose_name
        self.assertEquals(field_label, 'oldest completed date')

    def test_edited_workout_text_label(self):
        workout = Workout.objects.get(id=1)
        instance = WorkoutInstance.objects.get(workout=workout)
        field_label = instance._meta.get_field('edited_workout_text').verbose_name
        self.assertEquals(field_label, 'edited workout text')

    def test_scaling_text_label(self):
        workout = Workout.objects.get(id=1)
        instance = WorkoutInstance.objects.get(workout=workout)
        field_label = instance._meta.get_field('edited_scaling_text').verbose_name
        self.assertEquals(field_label, 'edited scaling text')

    def test_edited_workout_text_max_length(self):
        workout = Workout.objects.get(id=1)
        instance = WorkoutInstance.objects.get(workout=workout)
        max_length = instance._meta.get_field('edited_workout_text').max_length
        self.assertEquals(max_length, 2000)

    def test_edited_scaling_text_max_length(self):
        workout = Workout.objects.get(id=1)
        instance = WorkoutInstance.objects.get(workout=workout)
        max_length = instance._meta.get_field('edited_scaling_text').max_length
        self.assertEquals(max_length, 4000)

    def test_object_name_is_workout_id(self):
        workout = Workout.objects.get(id=1)
        instance = WorkoutInstance.objects.get(workout=workout)
        expected_object_name = f'Workout {workout.id}'
        self.assertEquals(expected_object_name, str(instance))

    def test_object_name_is_deleted_if_workout_deleted(self):
        workout = Workout.objects.get(id=1)
        instance = WorkoutInstance.objects.get(workout=workout)
        instance.workout = None
        expected_object_name = f'Workout Deleted'
        self.assertEquals(expected_object_name, str(instance))

    def test_get_absolute_url(self):
        workout = Workout.objects.get(id=1)
        instance = WorkoutInstance.objects.get(workout=workout)
        self.assertEquals(instance.get_absolute_url(), '/metcons/' + instance.current_user.username + '/workout/' + str(instance.id) + '/')

    def test_update_edited_workout_text(self):
        workout = Workout.objects.get(id=1)
        instance = WorkoutInstance.objects.get(workout=workout)
        instance.update_edited_workout_text()
        self.assertEquals(instance.edited_workout_text, instance.workout.workout_text)

    def test_update_edited_scaling_text(self):
        workout = Workout.objects.get(id=1)
        instance = WorkoutInstance.objects.get(workout=workout)
        instance.update_edited_scaling_text()
        self.assertEquals(instance.edited_scaling_text, instance.workout.scaling_or_description_text)

    def test_add_date_completed_if_date_doesnt_exist(self):
        workout = Workout.objects.get(id=1)
        instance = WorkoutInstance.objects.get(workout=workout)
        date = timezone.localtime(timezone.now()).date()
        instance.add_date_completed(date)
        date_object = Date.objects.filter(id=1)
        self.assertTrue(date_object.exists())
        date_completed_in_instance = None
        for i in instance.dates_workout_completed.all():
            date_completed_in_instance = i.date_completed
        self.assertEquals(date_completed_in_instance, date)
        self.assertEquals(instance.oldest_completed_date.date_completed, date)
        self.assertEquals(instance.youngest_scheduled_date, None)

    def test_add_date_completed_if_date_does_exist_ensuring_duplicates_arent_created(self):
        workout = Workout.objects.get(id=1)
        instance = WorkoutInstance.objects.get(workout=workout)
        date = timezone.localtime(timezone.now()).date()
        Date.objects.create(date_completed=date)
        instance.add_date_completed(date)
        number_of_date_objects = Date.objects.all().count()
        self.assertEquals(number_of_date_objects, 1)

    def test_add_date_to_be_completed_if_date_doesnt_exist(self):
        workout = Workout.objects.get(id=1)
        instance = WorkoutInstance.objects.get(workout=workout)
        date = timezone.localtime(timezone.now()).date()
        instance.add_date_to_be_completed(date)
        date_object = Date.objects.filter(id=1)
        self.assertTrue(date_object.exists())
        date_to_be_completed_in_instance = None
        for i in instance.dates_to_be_completed.all():
            date_to_be_completed_in_instance = i.date_completed
        self.assertEquals(date_to_be_completed_in_instance, date)
        self.assertEquals(instance.youngest_scheduled_date.date_completed, date)
        self.assertEquals(instance.oldest_completed_date, None)

    def test_add_date_to_be_completed_if_date_does_exist_ensuring_duplicates_arent_created(self):
        workout = Workout.objects.get(id=1)
        instance = WorkoutInstance.objects.get(workout=workout)
        date = timezone.localtime(timezone.now()).date()
        Date.objects.create(date_completed=date)
        instance.add_date_to_be_completed(date)
        number_of_date_objects = Date.objects.all().count()
        self.assertEquals(number_of_date_objects, 1)

    def test_remove_date_completed_if_date_exists_and_is_in_instance_dates_workout_completed(self):
        workout = Workout.objects.get(id=1)
        instance = WorkoutInstance.objects.get(workout=workout)
        date = timezone.localtime(timezone.now()).date()
        Date.objects.create(date_completed=date)
        date_object = Date.objects.get(id=1)
        instance.dates_workout_completed.add(date_object)
        self.assertTrue(Date.objects.filter(date_completed=date).exists())
        self.assertTrue(instance.dates_workout_completed.all().exists())
        self.assertEquals(instance.oldest_completed_date, None)
        self.assertEquals(instance.youngest_scheduled_date, None)
        instance.remove_date_completed(date)
        self.assertFalse(instance.dates_workout_completed.all().exists())
        self.assertEquals(instance.oldest_completed_date, None)
        self.assertEquals(instance.youngest_scheduled_date, None)

    def test_remove_date_completed_if_date_exists_and_in_instance_dates_workout_completed_and_is_oldest_scheduled_date(self):
        workout = Workout.objects.get(id=1)
        instance = WorkoutInstance.objects.get(workout=workout)
        date = timezone.localtime(timezone.now()).date()
        Date.objects.create(date_completed=date)
        date_object = Date.objects.get(id=1)
        instance.dates_workout_completed.add(date_object)
        instance.oldest_completed_date = date_object
        self.assertTrue(Date.objects.filter(date_completed=date).exists())
        self.assertTrue(instance.dates_workout_completed.all().exists())
        self.assertEquals(instance.oldest_completed_date.date_completed, date)
        instance.remove_date_completed(date)
        self.assertFalse(instance.dates_workout_completed.all().exists())
        self.assertEquals(instance.oldest_completed_date, None)
        self.assertEquals(instance.youngest_scheduled_date, None)

    def test_remove_date_completed_if_date_exists_and_is_not_in_instance_dates_workout_completed(self):
        workout = Workout.objects.get(id=1)
        instance = WorkoutInstance.objects.get(workout=workout)
        date = timezone.localtime(timezone.now()).date()
        Date.objects.create(date_completed=date)
        date_object = Date.objects.get(id=1)
        self.assertTrue(Date.objects.filter(date_completed=date).exists())
        self.assertFalse(instance.dates_workout_completed.all().exists())
        self.assertEquals(instance.oldest_completed_date, None)
        self.assertEquals(instance.youngest_scheduled_date, None)
        instance.remove_date_completed(date)
        self.assertFalse(instance.dates_workout_completed.all().exists())
        self.assertEquals(instance.oldest_completed_date, None)
        self.assertEquals(instance.youngest_scheduled_date, None)

    def test_remove_date_completed_if_date_doesnt_exist(self):
        workout = Workout.objects.get(id=1)
        instance = WorkoutInstance.objects.get(workout=workout)
        date = timezone.localtime(timezone.now()).date()
        self.assertFalse(Date.objects.all().exists())
        self.assertFalse(instance.dates_workout_completed.all().exists())
        self.assertEquals(instance.oldest_completed_date, None)
        self.assertEquals(instance.youngest_scheduled_date, None)
        instance.remove_date_completed(date)
        self.assertFalse(Date.objects.all().exists())
        self.assertFalse(instance.dates_workout_completed.all().exists())
        self.assertEquals(instance.oldest_completed_date, None)
        self.assertEquals(instance.youngest_scheduled_date, None)

    def test_remove_date_to_be_completed_is_none_if_date_exists_and_is_in_instance_dates_to_be_completed(self):
        workout = Workout.objects.get(id=1)
        instance = WorkoutInstance.objects.get(workout=workout)
        date = timezone.localtime(timezone.now()).date()
        Date.objects.create(date_completed=date)
        date_object = Date.objects.get(id=1)
        instance.dates_to_be_completed.add(date_object)
        self.assertTrue(Date.objects.filter(date_completed=date).exists())
        self.assertTrue(instance.dates_to_be_completed.all().exists())
        self.assertEquals(instance.youngest_scheduled_date, None)
        instance.remove_date_to_be_completed(date)
        self.assertFalse(instance.dates_to_be_completed.all().exists())
        self.assertEquals(instance.youngest_scheduled_date, None)

    def test_remove_date_to_be_completed_is_none_and_youngest_scheduled_date_is_none_if_date_exists_and_is_in_instance_dates_to_be_completed_and_is_youngest_scheduled_date(self):
        workout = Workout.objects.get(id=1)
        instance = WorkoutInstance.objects.get(workout=workout)
        date = timezone.localtime(timezone.now()).date()
        Date.objects.create(date_completed=date)
        date_object = Date.objects.get(id=1)
        instance.dates_to_be_completed.add(date_object)
        instance.youngest_scheduled_date = date_object
        self.assertTrue(Date.objects.filter(date_completed=date).exists())
        self.assertTrue(instance.dates_to_be_completed.all().exists())
        self.assertEquals(instance.youngest_scheduled_date.date_completed, date)
        instance.remove_date_to_be_completed(date)
        self.assertFalse(instance.dates_to_be_completed.all().exists())
        self.assertEquals(instance.youngest_scheduled_date, None)

    def test_remove_date_to_be_completed_does_nothing_if_date_exists_and_is_not_in_instance_dates_to_be_completed(self):
        workout = Workout.objects.get(id=1)
        instance = WorkoutInstance.objects.get(workout=workout)
        date = timezone.localtime(timezone.now()).date()
        Date.objects.create(date_completed=date)
        self.assertTrue(Date.objects.filter(date_completed=date).exists())
        self.assertFalse(instance.dates_to_be_completed.all().exists())
        self.assertEquals(instance.youngest_scheduled_date, None)
        instance.remove_date_to_be_completed(date)
        self.assertFalse(instance.dates_to_be_completed.all().exists())
        self.assertEquals(instance.youngest_scheduled_date, None)
        self.assertTrue(Date.objects.filter(date_completed=date).exists())

    def test_remove_date_to_be_completed_does_nothing_if_date_doesnt_exist(self):
        workout = Workout.objects.get(id=1)
        instance = WorkoutInstance.objects.get(workout=workout)
        date = timezone.localtime(timezone.now()).date()
        self.assertFalse(Date.objects.filter(date_completed=date).exists())
        self.assertFalse(instance.dates_to_be_completed.all().exists())
        self.assertEquals(instance.youngest_scheduled_date, None)
        instance.remove_date_to_be_completed(date)
        self.assertFalse(instance.dates_to_be_completed.all().exists())
        self.assertEquals(instance.youngest_scheduled_date, None)
        self.assertFalse(Date.objects.filter(date_completed=date).exists())

    def test_update_youngest_scheduled_date_is_none_if_is_youngest_scheduled_date_but_not_in_dates_to_be_completed(self):
        workout = Workout.objects.get(id=1)
        instance = WorkoutInstance.objects.get(workout=workout)
        date = timezone.localtime(timezone.now()).date() + timezone.timedelta(days=1)
        Date.objects.create(date_completed=date)
        date_object = Date.objects.get(id=1)
        instance.youngest_scheduled_date = date_object
        self.assertEquals(instance.youngest_scheduled_date.date_completed, date)
        instance.update_youngest_scheduled_date()
        self.assertEquals(instance.youngest_scheduled_date, None)

    def test_update_youngest_scheduled_date_is_date_if_dates_to_be_completed_is_in_future(self):
        workout = Workout.objects.get(id=1)
        instance = WorkoutInstance.objects.get(workout=workout)
        date = timezone.localtime(timezone.now()).date() + timezone.timedelta(days=1)
        Date.objects.create(date_completed=date)
        date_object = Date.objects.get(id=1)
        instance.dates_to_be_completed.add(date_object)
        self.assertEquals(instance.youngest_scheduled_date, None)
        self.assertTrue(instance.dates_to_be_completed.all().exists())
        instance.update_youngest_scheduled_date()
        self.assertEquals(instance.youngest_scheduled_date.date_completed, date)

    def test_update_youngest_scheduled_date_is_none_if_date_to_be_completed_is_in_past(self):
        workout = Workout.objects.get(id=1)
        instance = WorkoutInstance.objects.get(workout=workout)
        date = timezone.localtime(timezone.now()).date() - timezone.timedelta(days=1)
        Date.objects.create(date_completed=date)
        date_object = Date.objects.get(id=1)
        instance.dates_to_be_completed.add(date_object)
        self.assertEquals(instance.youngest_scheduled_date, None)
        self.assertTrue(instance.dates_to_be_completed.all().exists())
        instance.update_youngest_scheduled_date()
        self.assertEquals(instance.youngest_scheduled_date, None)
