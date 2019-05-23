Run remove_old_scheduled_dates.py everyday

Edited files on 5/22/2019:
(haven't uploaded at home)
created remove_old_scheduled_dates.py in rootdir
views.py
models.py doesn't require anything
forms.py
user_page.html
workoutinstance_detail.html
workout_detail.html
schedule_instance.html

Functionality completed on 5/22/2019:
- fixed date display. need to pass as filter not attribute
        - somedate|date:"format" not somedate.date
- changed workoutinstancecompleteddate to have default of timezone.localtime
- changed save function of result to add wicd to instance as timezone.localtime.date
        - if doing timezone.date instead it will save the date from UTC date which will be wrong (ahead of my localtime)
- change date_workout_completed on create result form to just DateField
        - result form now has an initial date of today and then if a different date is chosen the "time" of that date is set to 0:00
                - if the value is left as today then the timezone.now() datetime is used.
- added dates_to_be_completed field to instance model
- addded view and templates and form for scheduling workout
- change user_page.html to show future workouts
        - requires passing future workouts to the view
- cannot use result model to schedule workouts for the future.
        - might have to create new manytomany field on instances that is date_to_be_completed
                - many to many field allows workout to be scheduled multiple times in the future
                - can schedule same workout over and over again for the next weeks/months/whatever
        - this would allow any workout that has a date_to_be_completed to be put on the "future workouts" tab
                - for i in instance.date_to_be_completed.all(): if i > timezone.now(), put on future tab then break.
                        - may be a faster way to write this but this would work.
                - maybe instead of the for loop do:
                        - future workouts = wi.objects.filter(dates_to_be_completed__date_completed__gte=timezone.now()).distinct()
                                - might need to add an annotate before the filter to be able to order properly after
                                - timezone.now() must be created already [now = timezone.now()] then pass now in to filter
                        - do this in views then pass future_workouts to context
        - "past workouts" tab will order by recently completed dates.
                - will only update if people put results in but thats okay.
                        - ?how are they ordered if past results date_workout_completed are all the same time? (time= 0:00)
        - add a add_date_to_be_completed() function to model similar to add_date_completed()
        - ?add a delete_date_to_be_completed() function that removes dates to be completed from the instance if in the past?
                - can call every time instance is saved currently but in future would happen at midnight or weekly
- add a tabbed view on user page
        - one for future workouts that are planned
        - one for recent past workouts (within 2 weeks using dates_workout_completed)
                - recent_workouts = wi.objects.filter(dates_workout_completed__date_completed__lt=timezone.now(),
                                                      dates_workout_completed__date_completed__gtetimezone.now() - timedelta(days=14))
                                                                                                                        .distinct()
                        - timezone.now() must be created already [now = timezone.now()] then pass now in to filter
                                - timezone.timedelta as well
                - pass to views context as recently_completed_workouts
        - one for long past workouts (2+ weeks back using dates_workout_completed)
                - same as above as long_past_workouts
        - ordering will likely require annotates (see current user profile view)
        - order future workouts by closeness to today (opposite of how user profile is currently ordered [
                - .annotate(min_date=Min('dates_to_be_completed__date_completed').filter().order_by('min_date')
                        - may need (-) on order_by('min_date')
        - order past workouts by most recent (currently how user profile is ordered)
- get rid of classification and movements on workout and instance detail pages.
- get rid of dates on workout and instance detail pages
- add date of last completed to instance detail page next to workout title
        - "Workout 278 - *greyed out*Last Completed: Date*greyed out*
- fix get_earliest_to_completed date in instance model.
        - forgot to add .date() to the end so it was returning the model not the actual date
- add a line on the schedule workout page that says "by the way, you have this workout scheduled for:... dates"
- changed forms initial date on resultform and scheduled date to be timezone dependent (was UTC timezone.now)

Notes:
- work computer currently has issues displaying video. it will display fine but the command window will show errors that
        "an established connection was aborted by the software in your host machine"
        - happened on home computer but not first time page/video was viewed. (idk whats going on)
        - maybe this has to do with the video not being saved to cache properly
                - pictures save to cache and get response 304 when viewed multiple times, the video is getting 200 everytime
- currently slow to load metcons/workouts because it is not paginated and is loading all workouts in the database
- can't use onetoone between user and workoutinstance because then they can't have multiple workouts. has to be foreign key and create
        some restriction where if the workoutinstance with that specific workout already exists for that user it just pulls that up.
        this will likely have to be handled in the views.py
- to allow urls to extend with info, the get_absolute_url function must be in the model isntance and you must pass the arguments
        for each specification before it. otherwise you will get a reverse match not found on the template link.
        - see workout instance get_absolute_url for example
        - if using function based views, the argument must also be passed in the view function
                - see profile view as example
                - class based views take this into account with the models get_aboslute_url
- need to pass date as filter in template to display local time: somedate|date:"format" instead of somedate.date
        
Functionality to add:
- run remove_dates_to_be_completed_in_past() on instances everyday.
        - the reason this needs to be done is if someone has a workout scheduled in the future and in the past it will
                show up first on the scheduled workouts list and have a scheduled for date in the past.
        - one solution to this is to change dates_to_be_completed to be a foreign key and only allow scheduling once at a time
- to avoid having to remove dates to be completed everyday, figure out a way to order by and get the "min" date that is still
        greater than or equal to today.
        
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
- create a calendar dropdown for scheduling workouts
        - when you try and schedule a workout again you should have the dates highlighted that it is already scheduled
        - and have a line detailing that highlighted dates have already been scheduled
- move "last completed" on instancedetail page to next to the title like so:
        Workout 287 - Last Completed: Date
        - Grey the text for last completed out and make it smaller than workout number.
