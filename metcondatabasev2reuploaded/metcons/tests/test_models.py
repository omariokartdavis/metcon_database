from django.test import TestCase
from metcons.models import User, Classification, Movement, Workout, Date, WorkoutInstance, Result, ResultFile

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
        pull_up = Movement.objects.get(id=1)
        Workout.objects.create(workout_text='Pull Up', created_by_user=user)
        workout = Workout.objects.get(id=1)

    #test functions for adding pull up tag and updating classification
