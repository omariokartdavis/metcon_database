When deleting database: delete db and migrations. Run: makemigrations. migrate. createsuperuser. movements_list. mainsite_workouts.

# Run update_instance_dates and update_instance_hidden every day

## 6/24/19
(uploaded at work)
- test_models.py
- models.py (doesn't require anything)

## 6/25/29
(uploaded at work)
- movements_list.py
- test_models.py
- test_forms.py
- models.py (doesn't require anything)
- forms.py

## functionality completed on 6/24/19
- more model tests
- changed name of 2 variablse in instance functions to more clearly specify what it is

## functionality completed on 6/25/19
- finished model tests
- started and finished writing tests for forms
- changed some help texts in forms.py
- streamlined user create code in movements_list.py

#### Notes:
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
- to allow urls to extend with info, the get_absolute_url function must be in the model isntance and you must pass the arguments
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
        
## Functionality to add:
- add is_completed_rx and is_completed_scaled to result model?
- Create request model for athlete/coach requests
  - when adding a coach or athlete, send a request to that person.
  - have a confirmed booleanfield on model. when athlete/coach accepts, change it to true
  - requestee and requestor fields linked to user field
  - date field 
  - date confirmed field
  - where known from field (text field so can give a description of where they know each other)
  - requestor_is_coach boolean field
  - requestor_is_athlete boolean field
  - requestor_is_gym_owner boolean field
- gym owners need some distinction between adding athletes/coaches and adding members.k
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
- in add_athletes_to_coach view
  - change the add functionality so it sends a request to the athlete.
    - might need to create a "request-to-add" model
      - would contain info such as: athlete, coach, gym owner
      - then on requestee's page can have a popup that says 'coach' has claimed you as an athlete. 'Accept' 'Reject'
      - same for adding coach to athlete.
      - need some way to make this private so that people cannot request you, only you can request people
        - this way people don't get spammed
    - when the athlete accepts the request then add the athlete to the coach and vis-versa.
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
- add pagination to workout list, profile page, and instace detail page for results.
- this will likely solve itself when endless scroll is added
### For multiple sports:
- maybe just add a foreignkey field in current Workout model of "sport" that has different sport choices.
  -  should probably still create a different model for individual strength workout
    - holds one movement with as many sets/reps/weights as need
    - has manytomany with workout. (Should likely be a field in Workout model)
  - number of sets as integer field
    - this number from text input or dropdown would decide how many input boxes appear
      - use javascript to hide input boxes until this box losses focus
      - use javascript to prepopulate movement into boxes
      - use javascript to potentially include supersetting
      - have checkboxes for same weight for every set, same reps for every set so they can be autofilled
        - if supersetting they apply to each movement individually
          - (movement 1 all sets will have same weight and reps, movement 2 all sets will have same)
  - weights and reps as manytomany fields?
    - Weight model has value and unit
      -pre create common weights? 135/225/315/405lbs? 60/100/125/140kg?
    - reps can be pre created up to 50 just like movements/classifications
  - Would likely make filtering workout_list easier
  - All baseline fields in model like date_created and user can still be required.
                But all other defining fields will have to be not required
  - add all fields for all workouts to the current workout model (sets, reps, weights) and leave them as blank=True, null=True
  - on the create workout template, create a dropdown that can switch between different forms for different workout types
    - name all forms so the view can be seperated
    - have the default form be based on users default sport
    - could also just use multiple create workout buttons for different types. I like dropdown idea better if it can work
  - on the create_workout_view, handle the post requests based on form name
  - on the results and create_workout results, base the form and template off the workoutinstance.workout.sport with if statements
  - on the workout_list create a dropdown that can choose between any or all sports. default to users sport
- create a field on user model that has choices of different sports
  - whatever sport they choose will be their default createworkout model and default workout list to search through
  - choices: Crossfit, BB/Power/Strength Training/Oly (In the future: track, swimming, gymnastics?

## Styling:
- change color of workout name if assigned by coach or by self
- Create stylebook for all screens
- Create table for viewing workouts
        similar to the styling of this: https://fooplugins.github.io/FooTable/docs/examples/advanced/filter-dropdown.html
- Endless Scroll of workouts
- Add back button to previous search after filtering
- Add filters currently active below search boxes after a filter is chosen
- set maximum video and image size for displaying on webpage
- add click to hide/show scaling on workout detail and instance detail pages.
  - set default to hidden
- ?remove number of times completed counter from instance_detail page?
- style future/recent/past workouts as tabs on user page
  - default to future workouts if they have any, then recent, then past, then All Workouts if
                they have none scheduled and none completed
- create a calendar dropdown for scheduling workouts
  - when you try and schedule a workout again you should have the dates highlighted that it is already scheduled
  - and have a line detailing that highlighted dates have already been scheduled
- move "last completed" on instancedetail page to next to the title like so:
        Workout 287 - Last Completed: Date
  - Grey the text for last completed out and make it smaller than workout number.
- use jquery UI datepicker for date choices in schedule and result forms
  - look at top answer from this question: https://stackoverflow.com/questions/12884638/select-future-dates-only-django-form
  - can give available dates to schedule form and create result form
  - create result should only have past
  - schedule should only have future dates
