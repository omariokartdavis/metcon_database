When deleting database: delete db and migrations. Run: makemigrations. migrate. createsuperuser. movements_list. mainsite_workouts.

# Run all_update_funcs.py every day

# spelling mistake on remove_coach_or_athlete
- for remove athlete it says "Are you sure you would like to remove testathlete2 as one of *you* athletes?"

## 7/26/19
(uploaded at work)
- models.py (no migrations)
- urls.py
- views.py
- forms.py
- base_generic.css
- user_page.css
- create_workout.css
- create_workout.js
- user_page.js
- create_workout.html
- edit_schedule.html
- edit_schedule_for_multiple_athletes.html
- interim_created_workout.html
- interim_created_workout_for_multiple_athletes.html
- schedule_instance.html
- schedule_instance_for_multiple_athletes.html
- user_page.html
- workoutinstance_detail.html

## functionality completed on 7/26/19
- fixed issue with edit_schedule_for_multiple_athletes not going to correct url.
- added always visible scrollbar to all pages so there is no jarring center movement back and forth
- fixed dropdowncontainerworkoutbuttons always having a shadow even when not displayed
- fixed issue of create cardio workout not creating exercises past the first one
- changed cardio display on a lot of templates

#### Notes:
- sometimes django will not update css and javascript from seperate files because it thinks there has been no changes.
  - need to clear computers cache in order to force it to reload it.
- can add db_index=True to fields that get ordered_by/filtered_by a lot (date fields)
  - all foreignkey fields automatically have this, can remove it by db_index=False to save speed
  - might be a good idea as database gets bigger
- work computer currently has issues displaying video. it will display fine but the command window will show errors that
        "an established connection was aborted by the software in your host machine"
  - happened on home computer but not first time page/video was viewed. (idk whats going on)
  - maybe this has to do with the video not being saved to cache properly
    - pictures save to cache and get response 304 when viewed multiple times, the video is getting 200 everytime
- currently slow to load metcons/workouts because it is not paginated and is loading all workouts in the database
- workout 96 doesn't have a proper description. Scaling info is the description and scaling is none
  - not sure why it got pulled from the website this way.
  - same with Workout 266
- to allow urls to extend with info, the get_absolute_url function must be in the model instance and you must pass the arguments
        for each specification before it. otherwise you will get a reverse match not found on the template link.
  - see workout instance get_absolute_url for example
  - if using function based views, the argument must also be passed in the view function
    - see profile view as example
    - class based views take this into account with the models get_aboslute_url
- need to pass date as filter in template to display local time: somedate|date:"format" instead of somedate.date
- Date.objects.filter(dates_to_be_completed=instance, date_completed__gte=now).earliest('date_completed')
  - gives date object that is the earliest date from datestobecompleted from instance that also has date gte now
- can't get rid of distinct on user_page filters for future/recent/past workouts
  - if removed it will list every workout over and over again based on the number of dates it has in the future/recent/past
                but they will be ordered based on their youngest/oldest dates only. 
  - not necessary anyway
- athletes can still find out if a workout is hidden if they previously have the workout and go and schedule it for a future
  date past the current hidden date. It will then show on the calendar as being hidden and they will know that workout is scheduled
  - don't plan on doing anything to address this
        
## Functionality to add:
- check all views/templates and add info for cardio workouts
  - htmls: edit_instance, edit_result
  - views: edit_instance, edit_result
- edit strength instance form and cardio instance form should be nearly the same as the create forms
- add a "you have this workout set to unhide on: date" to interim schedule and schedule workouts pages if came from interim schedule
- may need to change edit_instance form for strength workouts
  - need to figure out editing comments for each strength exercise
- add a "You've already completed this workout" to workout list and include completed workouts by default
- change "schedule for all athletes buttons" to "schedule for multiple athletes"
  - then go to athlete select page and schedule select page
- change results for strength workout to use sets/reps/weights
- still need to handle result media files better
- put strength workouts in workout_list in workouts view 
- change createstrengthworkoutform to allow for varying reps per each set as well as weight
- can add a class if statement to the create_workout.html class="{% if user.default_sport == 'specific sport' %}default_form{%endif%}
- need to alter views (create workout view and all views that show info on workouts) to display properly if its a strength workout or general workout
- need to download itertools and use its chain function to combine querysets
  - may not need to do this since I modified WorkoutInstance to be for workouts and strength workouts
  - can use if instance.workout or if instance.strength_workout to diferentiate in templates etc.
  - may need this for workout_list view for combining both types of workout models
- don't forget to remove all "for testing purposes" code in templates like schedule_instance etc.
- add clean validation to create group form so that groups can't be created with the same name under the same user
- create all named workouts and create dropdown filter for them
  - can make a dropdown list of only named workouts
  - would likely add to movement_list.py or something
- change workoutinstance_detail so when sent to from calendar it shows only the results from that day
  - add a show all results button that then shows everything.
  - may not be able to do this as it is from a <a> get_absolute_url. would need to add a hidden input.
    - maybe change it to a form link that has action to the get_absolute_url so a hidden input can be included?
  - have to add in utils.py file in formatday() method f' string.
- on calendar view
  - add buttons that switch the view from day/week/month and can see more details of workouts on day/week than on month
- can create a notifications model
  - would only hold count of notifications
  - count can be an aggregate sum of requests currently and later any other things like messages etc.
- create edit group page to allow changing of group name
  - can also possibly combine add/delete athletes to group on this page
- add videos/pictures to movements to create a database of movement technique
- create tests for request, strengthworkout, strengthexercise, and set models
- break user sign up into two or more pages, first page has basic info (name, username, password, email, is athlete/coach etc)
  - second page can have more specific stuff based on their athlete/coach choice on first page
  - not sure which page should ask about sports, probably second
    - if athlete ask what sport they mainly focus on, if coach what sports do their athletes play and what sport do they play etc.
- add main_sport field to user model
- ?add is_completed_rx and is_completed_scaled to result model?
- gym owners need some distinction between adding athletes/coaches and adding members.
- if workout is_hidden and only has instances with users who all belong to the same coach/gym then don't show workout in workout list.
  - will have to be done on the workout_list query view.
- add more filters to schedule for all athletes and edit schedule for all athletes views.
  - can add filters for only workouts that were assigned by this coach
  - can add functionality for only athletes in a certain group with this workout
- add 'or user.gym_owner == instance.current_user.athlete.gym_owner' to all templates authentication
- add confirmed (default=False) field to coach/athlete/gym owner models
  - if coach adds an athlete it will add them to the coach so the coach can start writing workouts
    - nothing will show up on the athletes side until they accept the request
    - once request is accepted, change confirmed field to True and show all workouts coach has written for them.
- create 'tags' button on workout detail page that you can click 
  - will show you all movement and classification tags on that workout
- when a coach removes an athlete, send a notification to the athlete
- add user setting to change profile to a coach or gym owner
  - will create coach model and gym owner model for user and change users current flag from is_athlete to whatever
  - if changing from coach/gym owner to athlete simply chang ethe is_coach/gym_owner flag. Do not delete the coach/gymowner models
- create new view for a coach viewing their athletes workout instance?
  - workout name link from coaches page would link to new view instead of instance.get_absolute_url
  - new url would have coaches username then athletes username
  - new view could have athletes username on the page somewhere. everything else would likely be the same
  - would need all new buttons and views for each button to show coach username then athlete username
- clicking on an athletes workouts from the coaches page currently sends you to the athletes workoutinstance
  - I think this is okay but maybe change the url so it <coachusername>/athletes/<athleteusername>/instance
    - this would basically be creating a new page+url+view that has all the same stuff as the current instance view
      - may be unnecessary and can leave as is
- if user is athlete set workout default gender equal to user gender after user creation
- if user is coach leave workout default gender as both and simply ask if they want to change it (have form initial be both)
- ask users about their privacy settings or leave both and have popup on first going to profile page that shows them where
  they can change it.
- create add athlete/coach/gymowner via email functionality
  - send link to email address that will send them to the signup page possibly with their email already entered
  - can possibly have the person who sent the request add info about the requestee
    - gender, first name, last name etc.
- create profanity filter for creating workouts but not results
  - just like movement tags, create function to search for words in workout_text or scaling description
    - if words are found. delete that workout and give popup saying why
      - Popup: "This workout was removed from the database for adult language: (list of words used). Please refrain
          from using this language in your workout descriptions"
- create vote count for base workout
  - users can vote up someone elses user created workout if they downloaded it.
    - after a workout gains enough votes, it shows up in regular database searches.
  - write functions to increase vote count from instance
- ?create warning on user_created workouts list that these workouts have not been vetted for their programming?
- create dropdown filter for where workouts came from (users, mainsite, comptrain etc.)
- add ability to edit resultfiles on edit result page
- add filter for workout id on workout list page
- add create workout link to workout list page
  - under user authentication in template
- ?only update base workout times counted and duration at midnight?
  - will help speed up workout creation and all instance updates/saves
- add filter on workout instance detail page to filter results by date
- Add privacy setting so users can set their profile/workouts to private and therefore others cant search for/see them.
  - default to public
  - have a setting on each individual workout as well so users can make 1 workout public if they want but the rest of them stay private
  - public/private does not affect their coach seeing their workouts
- Combine Create Movement and Update Workout buttons into a popup:
  -on create movement button click open a popup to add movement. on save click run three functions:
    -save movement
    -update current workout
    -refresh page
- update Workout tags on all Workouts at midnight if there has been an added movement
- Better define the help text for creating a movement.
  - make sure it is clear how to type/format the word (title case, no hyphens or anything, words seperated by 1 space)
  - importance of proper classification
- Add some way to alert me when people add movements so I can check them.
  - can do this in the save function of movements. everytime a movement is saved send notification somehow
- Come up with a better way to list workouts instead of by workout number
  -add name to workout model or workoutinstance model and allow for blank/null. If name exists list by name otherwise list
                by "workout " + str(id)
  -would also change def `__str__` to if statement on if name exists otherwise same as above
### Pagination:
- add pagination to profile page.
  - not sure what exactly would be paginated.
    - this weeks workouts could maybe paginate by days?
    - recent and incomplete workouts could just paginate workouts
- add 'loading...' thing for infinite scroll
### For multiple sports:
- number of sets as integer field
  - this number from text input or dropdown would decide how many input boxes appear
    - use javascript to hide input boxes until this box losses focus
    - use javascript to prepopulate movement into boxes
    - use javascript to potentially include supersetting
    - have checkboxes for same weight for every set, same reps for every set so they can be autofilled
      - if supersetting they apply to each movement individually
        - (movement 1 all sets will have same weight and reps, movement 2 all sets will have same)
- on the create workout template, create a dropdown that can switch between different forms for different workout types
  - name all forms so the view can be seperated
  - have the default form be based on users default sport
  - could also just use multiple create workout buttons for different types. I like dropdown idea better if it can work
- on the create_workout_view, handle the post requests based on form name
- on the results and create_workout results, base the form and template off the workout/strengthworkout type
- on the workout_list create a dropdown that can choose between any or all sports. default to users sport
- create a field on user model that has choices of different sports
  - whatever sport they choose will be their default createworkout model and default workout list to search through
  - choices: Crossfit, BB/Power/Strength Training/Oly (In the future: track, swimming, gymnastics?)
- set up a strength workout model and strength program model
  - for strength programs, hold info about periodization rules etc. hold training maxes, days of the week when each workout ill be done
- create Training Maxes field on user model for eventual strength programs?

## Styling:
- in workoutinstance_detail style page so that workout is on left with results on right.
  - when you scroll workout should be fixed on left and results should scroll on right
- style workouts on calendar for if completed or not completed that day
  - if statement in utils on instance
    - if instance.dates_workout_completed.filter(date_completed=date).exists():
      - make names with extra class class="calendar_completed_workout_name"
- can add red dot to website icon on browser tab if you have notifications
  - (just like linkedin)
- parallax scrolling: https://www.w3schools.com/howto/howto_css_parallax.asp
- to have scrollbar, add height: somepixels; and overflow-y: auto; 
  - find out how to style scroll bar
  - add this as a hover style to an element to only show the scroll bar on hover
- css storage location: https://docs.djangoproject.com/en/2.2/intro/tutorial06/ `
- change color of workout name if assigned by coach or by self
  - already aplied the classes below. Just need to style them
    - .assigned_workout_name     .not_assigned_workout_name
- Create stylebook for all screens
- Create table for viewing workouts
        similar to the styling of this: https://fooplugins.github.io/FooTable/docs/examples/advanced/filter-dropdown.html
- Add back button to previous search after filtering
- Add filters currently active below search boxes after a filter is chosen
- set maximum video and image size for displaying on webpage
- add click to hide/show scaling on workout detail and instance detail pages.
  - set default to hidden
- ?remove number of times completed counter from instance_detail page?
- create a calendar dropdown for scheduling workouts
  - when you try and schedule a workout again you should have the dates highlighted that it is already scheduled
  - and have a line detailing that highlighted dates have already been scheduled
- move "last completed" on instancedetail page to next to the title like so:
        Workout 287 - Last Completed: Date
  - this is likely a display: inline
  - Grey the text for last completed out and make it smaller than workout number.
- use jquery UI datepicker for date choices in schedule and result forms
  - look at top answer from this question: https://stackoverflow.com/questions/12884638/select-future-dates-only-django-form
  - can give available dates to schedule form and create result form
  - create result should only have past
  - schedule should only have future dates
- on calendar tab for workouts:
  - create a large calendar that holds all past and future workouts by day.
- infinite scroll:
  - https://simpleisbetterthancomplex.com/tutorial/2017/03/13/how-to-create-infinite-scroll-with-django.html
- user_page calendar:
  - https://www.huiwenteo.com/normal/2018/07/24/django-calendar.html
  - https://alexpnt.github.io/2017/07/15/django-calendar/
- wrap the top bar on base generic in the blue div so that they are all fixed
  - this does not work!
  
# Mobile App:
- when clicking a workout either on user_page or workout_list, show buttons underneath workout after its touched
  - just like reddit with "comments, share, ... "etc
- https://www.quora.com/How-do-we-convert-the-Django-web-application-into-an-Android-app
- on users this weeks workouts page
  - swipe left/right for different days
- notes on creating mobile app with django as server side backend:
  - create a mobile app using java (java is frontend just like html) then use django rest framework to communicate with backend
  - https://stackoverflow.com/questions/24402017/django-how-to-integrate-django-rest-framework-in-an-existing-application
  - https://www.django-rest-framework.org/tutorial/1-serialization/
  - https://stackoverflow.com/questions/19217835/can-an-android-app-connect-directly-to-an-online-mysql-database
  - https://www.quora.com/How-do-we-convert-the-Django-web-application-into-an-Android-app
