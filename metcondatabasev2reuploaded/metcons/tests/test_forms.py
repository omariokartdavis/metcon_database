from django.test import SimpleTestCase, TestCase
from metcons.forms import *
from django.utils import timezone

class SignUpFormTest(SimpleTestCase):
    def test_first_name_field_label(self):
        form = SignUpForm()
        self.assertTrue(form.fields['first_name'].label == None or form.fields['first_name'].label == 'first name')

    def test_last_name_field_label(self):
        form = SignUpForm()
        self.assertTrue(form.fields['last_name'].label == None or form.fields['last_name'].label == 'last name')

    def test_email_field_label(self):
        form = SignUpForm()
        self.assertTrue(form.fields['email'].label == None or form.fields['email'].label == 'email')

    def test_athlete_status_field_label(self):
        form = SignUpForm()
        self.assertTrue(form.fields['athlete_status'].label == None or form.fields['athlete_status'].label == 'athlete status')

    def test_gender_field_label(self):
        form = SignUpForm()
        self.assertTrue(form.fields['gender'].label == None or form.fields['gender'].label == 'gender')

    def test_default_workout_gender_field_label(self):
        form = SignUpForm()
        self.assertTrue(form.fields['default_workout_gender'].label == None or form.fields['default_workout_gender'].label == 'default workout gender')

    def test_athlete_status_help_text(self):
        form = SignUpForm()
        self.assertEquals(form.fields['athlete_status'].help_text, 'Selecting Coach or Gym Owner will also sign you up as an athlete.')

    def test_default_workout_gender_help_text(self):
        form = SignUpForm()
        self.assertEquals(form.fields['default_workout_gender'].help_text, 'What is the gender that you will most often write workouts for? This will be the default gender chosen when you create a workout; however, you can change this during creation of any workout.')

class AddAthleteToCoachFormTest(SimpleTestCase):
    def test_athlete_username_field_label(self):
        form = AddAthleteToCoachForm()
        self.assertTrue(form.fields['athlete_username'].label == None or form.fields['athlete_username'].label == 'athlete username')

    def test_athlete_username_help_text(self):
        form = AddAthleteToCoachForm()
        self.assertEquals(form.fields['athlete_username'].help_text, 'What is the athletes username? Lowercase letters only.')

class RemoveAthleteFromCoachFormTest(SimpleTestCase):
    def test_athlete_to_remove_field_label(self):
        form = RemoveAthleteFromCoachForm()
        self.assertTrue(form.fields['athlete_to_remove'].label == None or form.fields['athlete_to_remove'].label == 'athlete to remove')

    def test_athlete_to_remove_help_text(self):
        form = RemoveAthleteFromCoachForm()
        self.assertEquals(form.fields['athlete_to_remove'].help_text, 'Which athletes would you like to remove?')

class AddCoachFormTest(SimpleTestCase):
    def test_coach_username_field_label(self):
        form = AddCoachForm()
        self.assertTrue(form.fields['coach_username'].label == None or form.fields['coach_username'].label == 'coach username')

    def test_coach_username_help_text(self):
        form = AddCoachForm()
        self.assertEquals(form.fields['coach_username'].help_text, 'What is the coaches username? Lowercase letters only.')

class RemoveCoachFromAthleteFormTest(SimpleTestCase):
    def test_coach_username_field_label(self):
        form = RemoveCoachFromAthleteForm()
        self.assertTrue(form.fields['coach_to_remove'].label == None or form.fields['coach_to_remove'].label == 'coach to remove')

    def test_coach_username_help_text(self):
        form = RemoveCoachFromAthleteForm()
        self.assertEquals(form.fields['coach_to_remove'].help_text, 'Which coach would you like to remove?')

class AddWorkoutToAthletesFormTest(SimpleTestCase):
    def test_athlete_to_assign_field_label(self):
        form =  AddWorkoutToAthletesForm()
        self.assertTrue(form.fields['athlete_to_assign'].label == None or form.fields['athlete_to_assign'].label == 'athlete to assign')

    def test_group_to_assign_field_label(self):
        form =  AddWorkoutToAthletesForm()
        self.assertTrue(form.fields['group_to_assign'].label == None or form.fields['group_to_assign'].label == 'group to assign')

    def test_hide_from_athletes_field_label(self):
        form =  AddWorkoutToAthletesForm()
        self.assertTrue(form.fields['hide_from_athletes'].label == None or form.fields['hide_from_athletes'].label == 'hide from athletes')

    def test_date_to_unhide_field_label(self):
        form =  AddWorkoutToAthletesForm()
        self.assertTrue(form.fields['date_to_unhide'].label == None or form.fields['date_to_unhide'].label == 'date to unhide')

    def test_athlete_to_assign_help_text(self):
        form = AddWorkoutToAthletesForm()
        self.assertEquals(form.fields['athlete_to_assign'].help_text, 'Which athletes would you like to assign this workout to?')

    def test_hide_from_athletes_help_text(self):
        form = AddWorkoutToAthletesForm()
        self.assertEquals(form.fields['hide_from_athletes'].help_text, 'Would you like to hide the details of this workout from assigned athletes until a specified date?')

    def test_group_to_assign_help_text(self):
        form = AddWorkoutToAthletesForm()
        self.assertEquals(form.fields['group_to_assign'].help_text, 'Which groups would you like to assign this workout to?')

    def test_date_to_unhide_help_text(self):
        form = AddWorkoutToAthletesForm()
        self.assertEquals(form.fields['date_to_unhide'].help_text, 'When would you like to unhide this workout?')

class CreateGroupFormTest(SimpleTestCase):
    def test_group_name_field_label(self):
        form =  CreateGroupForm()
        self.assertTrue(form.fields['group_name'].label == None or form.fields['group_name'].label == 'group name')

    def test_athlete_to_add_field_label(self):
        form =  CreateGroupForm()
        self.assertTrue(form.fields['athlete_to_add'].label == None or form.fields['athlete_to_add'].label == 'athlete to add')

    def test_athlete_to_add_help_text(self):
        form = CreateGroupForm()
        self.assertEquals(form.fields['athlete_to_add'].help_text, 'Which athletes would you like to add to this group?')

class AddAthletesToGroupFormTest(SimpleTestCase):
    def test_athlete_to_add_field_label(self):
        form =  AddAthletesToGroupForm()
        self.assertTrue(form.fields['athlete_to_add'].label == None or form.fields['athlete_to_add'].label == 'athlete to add')

    def test_athlete_to_add_help_text(self):
        form = AddAthletesToGroupForm()
        self.assertEquals(form.fields['athlete_to_add'].help_text, 'Which athletes would you like to add to this group?')

class RemoveAthletesFromGroupFormTest(SimpleTestCase):
    def test_athlete_to_remove_field_label(self):
        form =  RemoveAthletesFromGroupForm()
        self.assertTrue(form.fields['athlete_to_remove'].label == None or form.fields['athlete_to_remove'].label == 'athlete to remove')

    def test_athlete_to_remove_help_text(self):
        form = RemoveAthletesFromGroupForm()
        self.assertEquals(form.fields['athlete_to_remove'].help_text, 'Which athletes would you like to remove from this group?')

class CreateWorkoutFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='odavis', password='4a0308ki9ps')
        
    def test_workout_text_field_label(self):
        user = User.objects.get(id=1)
        form =  CreateWorkoutForm(**{'user':user})
        self.assertTrue(form.fields['workout_text'].label == None or form.fields['workout_text'].label == 'workout text')

    def test_workout_scaling_field_label(self):
        user = User.objects.get(id=1)
        form =  CreateWorkoutForm(**{'user':user})
        self.assertTrue(form.fields['workout_scaling'].label == None or form.fields['workout_scaling'].label == 'workout scaling')

    def test_estimated_duration_field_label(self):
        user = User.objects.get(id=1)
        form =  CreateWorkoutForm(**{'user':user})
        self.assertTrue(form.fields['estimated_duration'].label == None or form.fields['estimated_duration'].label == 'estimated duration')

    def test_gender_field_label(self):
        user = User.objects.get(id=1)
        form =  CreateWorkoutForm(**{'user':user})
        self.assertTrue(form.fields['gender'].label == None or form.fields['gender'].label == 'gender')

    def test_athlete_to_assign_field_label_if_user_is_coach(self):
        user = User.objects.get(id=1)
        user.is_coach = True
        user.save()
        form = CreateWorkoutForm(**{'user':user})
        self.assertTrue(form.fields['athlete_to_assign'].label == None or form.fields['athlete_to_assign'].label == 'athlete to assign')

    def test_group_to_assign_field_label_if_user_is_coach(self):
        user = User.objects.get(id=1)
        user.is_coach = True
        user.save()
        form =  CreateWorkoutForm(**{'user':user})
        self.assertTrue(form.fields['group_to_assign'].label == None or form.fields['group_to_assign'].label == 'group to assign')

    def test_hide_from_athletes_field_label_if_user_is_coach(self):
        user = User.objects.get(id=1)
        user.is_coach = True
        user.save()
        form =  CreateWorkoutForm(**{'user':user})
        self.assertTrue(form.fields['hide_from_athletes?'].label == None or form.fields['hide_from_athletes'].label == 'hide from athletes')

    def test_date_to_unhide_field_label_if_user_is_coach(self):
        user = User.objects.get(id=1)
        user.is_coach = True
        user.save()
        form =  CreateWorkoutForm(**{'user':user})
        self.assertTrue(form.fields['date_to_unhide'].label == None or form.fields['date_to_unhide'].label == 'date to unhide')

    def test_athlete_to_assign_field_label_if_user_is_gym_owner(self):
        user = User.objects.get(id=1)
        user.is_gym_owner = True
        user.save()
        form = CreateWorkoutForm(**{'user':user})
        self.assertTrue(form.fields['athlete_to_assign'].label == None or form.fields['athlete_to_assign'].label == 'athlete to assign')

    def test_group_to_assign_field_label_if_user_is_gym_owner(self):
        user = User.objects.get(id=1)
        user.is_gym_owner = True
        user.save()
        form =  CreateWorkoutForm(**{'user':user})
        self.assertTrue(form.fields['group_to_assign'].label == None or form.fields['group_to_assign'].label == 'group to assign')

    def test_hide_from_athletes_field_label_if_user_is_gym_owner(self):
        user = User.objects.get(id=1)
        user.is_gym_owner = True
        user.save()
        form =  CreateWorkoutForm(**{'user':user})
        self.assertTrue(form.fields['hide_from_athletes?'].label == None or form.fields['hide_from_athletes'].label == 'hide from athletes')

    def test_date_to_unhide_field_label_if_user_is_gym_owner(self):
        user = User.objects.get(id=1)
        user.is_gym_owner = True
        user.save()
        form =  CreateWorkoutForm(**{'user':user})
        self.assertTrue(form.fields['date_to_unhide'].label == None or form.fields['date_to_unhide'].label == 'date to unhide')

    def test_workout_text_max_length(self):
        user = User.objects.get(id=1)
        form =  CreateWorkoutForm(**{'user':user})
        max_length = form.fields['workout_text'].max_length
        self.assertEquals(max_length, 2000)

    def test_workout_scaling_max_length(self):
        user = User.objects.get(id=1)
        form =  CreateWorkoutForm(**{'user':user})
        max_length = form.fields['workout_scaling'].max_length
        self.assertEquals(max_length, 4000)
        
    def test_workout_text_help_text(self):
        user = User.objects.get(id=1)
        form =  CreateWorkoutForm(**{'user':user})
        self.assertEquals(form.fields['workout_text'].help_text, 'Enter your workout.')

    def test_workout_scaling_help_text(self):
        user = User.objects.get(id=1)
        form =  CreateWorkoutForm(**{'user':user})
        self.assertEquals(form.fields['workout_scaling'].help_text, 'Enter any scaling options.')
        
    def test_estimated_duration_help_text(self):
        user = User.objects.get(id=1)
        form =  CreateWorkoutForm(**{'user':user})
        self.assertEquals(form.fields['estimated_duration'].help_text, 'Enter an estimate of how long it will take to complete the workout in minutes (whole numbers only).')

    def test_gender_help_text(self):
        user = User.objects.get(id=1)
        form =  CreateWorkoutForm(**{'user':user})
        self.assertEquals(form.fields['gender'].help_text, 'Is this workout (and the weights you have entered) applicable for both Males and Females or only one?')

    def test_athlete_to_assign_help_text_if_user_is_coach(self):
        user = User.objects.get(id=1)
        user.is_coach = True
        user.save()
        form =  CreateWorkoutForm(**{'user':user})
        self.assertEquals(form.fields['athlete_to_assign'].help_text, 'Which athletes would you like to assign this workout to?')

    def test_group_to_assign_help_text_if_user_is_coach(self):
        user = User.objects.get(id=1)
        user.is_coach = True
        user.save()
        form =  CreateWorkoutForm(**{'user':user})
        self.assertEquals(form.fields['group_to_assign'].help_text, 'Which groups would you like to assign this workout to?')

    def test_hide_from_athletes_help_text_if_user_is_coach(self):
        user = User.objects.get(id=1)
        user.is_coach = True
        user.save()
        form =  CreateWorkoutForm(**{'user':user})
        self.assertEquals(form.fields['hide_from_athletes?'].help_text, 'Would you like to hide the details of this workout from assigned athletes until a specified date?')

    def test_date_to_unhide_help_text_if_user_is_coach(self):
        user = User.objects.get(id=1)
        user.is_coach = True
        user.save()
        form =  CreateWorkoutForm(**{'user':user})
        self.assertEquals(form.fields['date_to_unhide'].help_text, 'When would you like to unhide this workout?')

    def test_athlete_to_assign_help_text_if_user_is_gym_owner(self):
        user = User.objects.get(id=1)
        user.is_gym_owner = True
        user.save()
        form =  CreateWorkoutForm(**{'user':user})
        self.assertEquals(form.fields['athlete_to_assign'].help_text, 'Which athletes would you like to assign this workout to?')

    def test_group_to_assign_help_text_if_user_is_gym_owner(self):
        user = User.objects.get(id=1)
        user.is_gym_owner = True
        user.save()
        form =  CreateWorkoutForm(**{'user':user})
        self.assertEquals(form.fields['group_to_assign'].help_text, 'Which groups would you like to assign this workout to?')

    def test_hide_from_athletes_help_text_if_user_is_gym_owner(self):
        user = User.objects.get(id=1)
        user.is_gym_owner = True
        user.save()
        form =  CreateWorkoutForm(**{'user':user})
        self.assertEquals(form.fields['hide_from_athletes?'].help_text, 'Would you like to hide the details of this workout from assigned athletes until a specified date?')

    def test_date_to_unhide_help_text_if_user_is_gym_owner(self):
        user = User.objects.get(id=1)
        user.is_gym_owner = True
        user.save()
        form =  CreateWorkoutForm(**{'user':user})
        self.assertEquals(form.fields['date_to_unhide'].help_text, 'When would you like to unhide this workout?')
        
class CreateResultFormTest(SimpleTestCase):
    def test_result_text_field_label(self):
        form =  CreateResultForm()
        self.assertTrue(form.fields['result_text'].label == None or form.fields['result_text'].label == 'result text')

    def test_duration_minutes_field_label(self):
        form =  CreateResultForm()
        self.assertTrue(form.fields['duration_minutes'].label == None or form.fields['duration_minutes'].label == 'duration minutes')

    def test_duration_seconds_field_label(self):
        form =  CreateResultForm()
        self.assertTrue(form.fields['duration_seconds'].label == None or form.fields['duration_seconds'].label == 'duration seconds')

    def test_media_file_field_label(self):
        form =  CreateResultForm()
        self.assertTrue(form.fields['media_file'].label == None or form.fields['media_file'].label == 'media file')

    def test_media_file_caption_field_label(self):
        form =  CreateResultForm()
        self.assertTrue(form.fields['media_file_caption'].label == None or form.fields['media_file_caption'].label == 'media file caption')

    def test_date_completed_field_label(self):
        form =  CreateResultForm()
        self.assertTrue(form.fields['date_completed'].label == None or form.fields['date_completed'].label == 'date completed')

    def test_result_text_max_length(self):
        form = CreateResultForm()
        max_length = form.fields['result_text'].max_length
        self.assertEquals(max_length, 2000)
        
    def test_result_text_help_text(self):
        form = CreateResultForm()
        self.assertEquals(form.fields['result_text'].help_text, 'Enter your results here.')

    def test_media_file_help_text(self):
        form = CreateResultForm()
        self.assertEquals(form.fields['media_file'].help_text, 'Attach any pictures or videos. Hold CTRL while selecting to upload multiple files.')

    def test_media_file_caption_help_text(self):
        form = CreateResultForm()
        self.assertEquals(form.fields['media_file_caption'].help_text, 'Caption your media file if applicable.')

    def test_date_completed_help_text(self):
        form = CreateResultForm()
        self.assertEquals(form.fields['date_completed'].help_text, 'When did you complete this workout?')

class ScheduleInstanceFormTest(SimpleTestCase):
    def test_date_to_be_added_field_label(self):
        form =  ScheduleInstanceForm()
        self.assertTrue(form.fields['date_to_be_added'].label == None or form.fields['date_to_be_added'].label == 'date to be added')

    def test_repeat_yes_field_label(self):
        form =  ScheduleInstanceForm()
        self.assertTrue(form.fields['repeat_yes'].label == None or form.fields['repeat_yes'].label == 'repeat yes')

    def test_repeat_frequency_field_label(self):
        form =  ScheduleInstanceForm()
        self.assertTrue(form.fields['repeat_frequency'].label == None or form.fields['repeat_frequency'].label == 'repeat frequency')

    def test_number_of_repetitions_field_label(self):
        form =  ScheduleInstanceForm()
        self.assertTrue(form.fields['number_of_repetitions'].label == None or form.fields['number_of_repetitions'].label == 'number of repetitions')

    def test_repeat_length_field_label(self):
        form =  ScheduleInstanceForm()
        self.assertTrue(form.fields['repeat_length'].label == None or form.fields['repeat_length'].label == 'repeat length')

    def test_date_to_be_added_help_text(self):
        form = ScheduleInstanceForm()
        self.assertEquals(form.fields['date_to_be_added'].help_text, 'When will you complete this workout?')

    def test_number_of_repetitions_help_text(self):
        form = ScheduleInstanceForm()
        self.assertEquals(form.fields['number_of_repetitions'].help_text, 'XX number of times to repeat.')

class EditScheduleFormTest(SimpleTestCase):
    def test_date_to_be_removed_field_label(self):
        form =  EditScheduleForm()
        self.assertTrue(form.fields['date_to_be_removed'].label == None or form.fields['date_to_be_removed'].label == 'date to be removed')

    def test_date_to_be_added_field_label(self):
        form =  EditScheduleForm()
        self.assertTrue(form.fields['date_to_be_added'].label == None or form.fields['date_to_be_added'].label == 'date to be added')

    def test_date_to_be_removed_help_text(self):
        form = EditScheduleForm()
        self.assertEquals(form.fields['date_to_be_removed'].help_text, 'What date would you like to remove?')

    def test_date_to_be_added_help_text(self):
        form = EditScheduleForm()
        self.assertEquals(form.fields['date_to_be_added'].help_text, 'When will you complete this workout?')

class DeleteScheduleFormTest(SimpleTestCase):
    def test_date_to_be_removed_field_label(self):
        form =  DeleteScheduleForm()
        self.assertTrue(form.fields['date_to_be_removed'].label == None or form.fields['date_to_be_removed'].label == 'date to be removed')

    def test_date_to_be_removed_help_text(self):
        form = DeleteScheduleForm()
        self.assertEquals(form.fields['date_to_be_removed'].help_text, 'What date would you like to remove?')

class HideInstanceFormTest(SimpleTestCase):
    def test_date_to_unhide_field_label(self):
        form =  HideInstanceForm()
        self.assertTrue(form.fields['date_to_unhide'].label == None or form.fields['date_to_unhide'].label == 'date to unhide')

    def test_date_to_unhide_help_text(self):
        form = HideInstanceForm()
        self.assertEquals(form.fields['date_to_unhide'].help_text, 'When would you like to unhide this workout?')

class EditInstanceFormTest(SimpleTestCase):
    def test_workout_text_field_label(self):
        form =  EditInstanceForm()
        self.assertTrue(form.fields['workout_text'].label == None or form.fields['workout_text'].label == 'workout text')

    def test_scaling_text_field_label(self):
        form =  EditInstanceForm()
        self.assertTrue(form.fields['scaling_text'].label == None or form.fields['scaling_text'].label == 'scaling text')

    def test_duration_minutes_field_label(self):
        form =  EditInstanceForm()
        self.assertTrue(form.fields['duration_minutes'].label == None or form.fields['duration_minutes'].label == 'duration minutes')

    def test_duration_seconds_field_label(self):
        form =  EditInstanceForm()
        self.assertTrue(form.fields['duration_seconds'].label == None or form.fields['duration_seconds'].label == 'duration seconds')

    def test_duration_minutes_negative(self):
        form = EditInstanceForm({'duration_minutes': -1, 'duration_seconds': 0})
        self.assertFalse(form.is_valid())

    def test_duration_minutes_positive(self):
        form = EditInstanceForm({'duration_minutes': 5, 'duration_seconds': 0})
        self.assertTrue(form.is_valid())

    def test_duration_seconds_negative(self):
        form = EditInstanceForm({'duration_seconds': -1, 'duration_minutes': 0})
        self.assertFalse(form.is_valid())

    def test_duration_seconds_positive(self):
        form = EditInstanceForm({'duration_seconds': 5, 'duration_minutes': 0})
        self.assertTrue(form.is_valid())

class EditResultFormTest(SimpleTestCase):
    def test_result_text_field_label(self):
        form =  EditResultForm()
        self.assertTrue(form.fields['result_text'].label == None or form.fields['result_text'].label == 'result text')

    def test_date_completed_field_label(self):
        form =  EditResultForm()
        self.assertTrue(form.fields['date_completed'].label == None or form.fields['date_completed'].label == 'date completed')

    def test_duration_minutes_field_label(self):
        form =  EditResultForm()
        self.assertTrue(form.fields['duration_minutes'].label == None or form.fields['duration_minutes'].label == 'duration minutes')

    def test_duration_seconds_field_label(self):
        form =  EditResultForm()
        self.assertTrue(form.fields['duration_seconds'].label == None or form.fields['duration_seconds'].label == 'duration seconds')

    def test_duration_minutes_negative(self):
        form = EditResultForm({'duration_minutes': -1, 'duration_seconds': 0, 'result_text': 'Text'})
        self.assertFalse(form.is_valid())

    def test_duration_minutes_positive(self):
        form = EditResultForm({'duration_minutes': 5, 'duration_seconds': 0, 'result_text': 'Text'})
        self.assertTrue(form.is_valid())

    def test_duration_seconds_negative(self):
        form = EditResultForm({'duration_seconds': -1, 'duration_minutes': 0, 'result_text': 'Text'})
        self.assertFalse(form.is_valid())

    def test_duration_seconds_positive(self):
        form = EditResultForm({'duration_seconds': 5, 'duration_minutes': 0, 'result_text': 'Text'})
        self.assertTrue(form.is_valid())
