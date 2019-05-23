When deleting database: delete db and migrations. Run: makemigrations. migrate. createsuperuser. movements_list. mainsite_workouts.
Edited files on 5/23/2019:
(haven't uploaded at home)
views.py

Functionality completed on 5/23/2019:
- added youngest_scheduled_date and oldest_completed_date fields to instance model
- order by youngest_scheduled_date and oldest_completed_date on user page
        - also displays those dates for scheduled for: completed on:
- added function to update youngest/oldest dates and call it on every save\
        - changed these functions to use database filters to be much faster
- added function to get all dates in future
        - for scheduled date form page to list dates in future scheduled.
- should no longer have to remove dates from dates_to_be_completed
        - might still want anyway
        - delete every one that is > 1 week old?
- changed order of result lists on instance detail page to be ordered by "-date_workout_completed" instead of "-date_created"
- added workout description to results add page
- change mainsite_workouts datetime to timezone.make_aware(datetime)
        - don't think I need localtime on this
- removed update functions from save function in instance and results
        - all update functions now live in the respective views.
- used .iterator() and .exists() on applicable functions
- changed update_youngest_scheduled_date to not fail if there is no option.
        instead sets to null
- changed user_profile view to exclude workouts from future workouts if:
        - the youngest_scheduled_date = date_workout_completed=today
                - this shouldn't ever happen due to the update_youngest_scheduled_date function but just in case
        - and exclude if youngest_scheduled_date is None/Null  
                - this is what should happen if the first statement was true in the update_youngest_date func
- added default value for duration in result create form
        - based on instance.duration. if exists it is equal to that. if not it is 0
- changed all users workouts list on user page to "Other workouts" and have it only list workouts that haven't been completed
        but also haven't been scheduled
        
Notes:
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
- to allow urls to extend with info, the get_absolute_url function must be in the model isntance and you must pass the arguments
        for each specification before it. otherwise you will get a reverse match not found on the template link.
        - see workout instance get_absolute_url for example
        - if using function based views, the argument must also be passed in the view function
                - see profile view as example
                - class based views take this into account with the models get_aboslute_url
- need to pass date as filter in template to display local time: somedate|date:"format" instead of somedate.date
- wicd.objects.filter(dates_to_be_completed=instance, date_completed__gte=now).earliest('date_completed')
        - gives wicd object that is the earliest date from datestobecompleted from instance that also has date gte now
- can't get rid of distinct on user_page filters for future/recent/past workouts
        - if removed it will list every workout over and over again based on the number of dates it has in the future/recent/past
                but they will be ordered based on their youngest/oldest dates only. 
        - not necessary anyway
        
Functionality to add:
- need to run update_instance_dates every new day
- add a Gender field to workouts that can be M/F/Both signifying if the weights are categorized for males/females
        - all crossfit mainsite workouts are both
        - ?could possibly do it just like movement tags instead of create a field?
                - could add Men, Women, Man, Woman to movement tags and have their classificaion be Gender or Male/Female
                        - probably better to do something similar but create new field in workout model anyway. simpler
- when creating update views and delete views make sure the view calls the proper update functions on each model because
        I took them out of the save functions.
- modify result delete method so it calls update_times completed on instance
        - do this in the delete view rather than the delete method.
                upon hitting delete, delete the result, then run updates like remove date completed etc.
- use jquery UI datepicker for date choices in schedule and result forms
        - look at top answer from this question: https://stackoverflow.com/questions/12884638/select-future-dates-only-django-form
        - can give available dates to schedule form and create result form
        - create result should only have past
        - schedule should only have future
- create a popup that asks if they completed a workout the previous day if it was scheduled but they didn't add a result.
        - have add result button that has default date of previous day
- add create workout link to workout list page
        - under user authentication in template
- add ability to schedule workout during workout creation
        - on workout create form have date field to schedule workout for (default today, just like result form)
        - take date and put it into date_to_be_completed of instance
- when creating a new workout, offer users a choice to add a result of this workout immediately.
        - popup: "Have you completed this workout recently (within last week)?" with links y/n
                - if y go to add results page/popup (need choice of when did you complete this workout)
                - if no go to instance detail page
- ?only update base workout times counted and duration at midnight?
        - will help speed up workout creation and all instance updates/saves
- add filter on workout instance detail page to filter results by date
- ?put filter searches on base_generic page and do {% block filters %}{% endblock %} if you don't want them to come up?
- only allow user who created base workout to edit that workout and only while no one else has added it to their page
        - if edited after others have it on their profile, it will change everyones workout.
        - if user == Workout.created_by_user (or user.username == Workout.created_by_user.username):
                - if not WorkoutInstance.objects.filter(workout=workout): allow edits
                - else: nah
- add click to edit button on workout instance detail page.
        - only edit fields specific to that instance aka duration completed, times completed, dates completed etc.
- Pagination:
        - add pagination to workout list, profile page, and instace detail page for results.
                - workout list pagination got removed becuase I changed it to a function view to allow POST forms
        - get rid of pagination on workout list if not logged in but keep it if logged in.
                - just adding block pagination endblock gets rid of pagination in both situations
        - this will likely solve itself when endless scroll is added
- add login to index page.
- Add search for a specific users workouts
        - search for workouts mat fraser has done
        - filter for workouts whose workout instances have users of xx name
                - maybe this is a subquery?
- Add privacy setting so users can set their profile/workouts to private and therefore others cant search for/see them.
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
        -would also change def __str__ to if statement on if name exists otherwise same as above
For multiple sports:
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

Styling:
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
