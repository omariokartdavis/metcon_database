Edited files on 5/22/2019:
(haven't uploaded at work)
models.py
workoutinstance_detail.html
workout_detail.html

Functionality completed on 5/22/2019:
- fixed date display. need to pass as filter not attribute
        - somedate|date:"format" not somedate.date
                
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
- undid workoutdetail.date and instance.date because its rounding dates forward to the next day.
        
Functionality to add:
- change result model function for adding date workout_completed to workoutinstance by:
        timezone.localtime(self.date_workout_completed).date
- change date_workout_completed on create result form to just DateField
        - add a time of midnight afterwards unless its today, then assume its timezone.now
- add ability to choose dates completed when creating workout
        - will be on the create workout form and will be used to create the instance off of that workout
- when creating a new workout, offer users a choice to add a result of this workout immediately.
        - popup: "Have you already completed this workout?" with linkes y/n
                - if y go to add results page/popup (need choice of when did you complete this workout)
                - if no go to instance detail page
- ?only update base workout times counted and duration at midnight?
- add click to hide/show scaling on workout detail and instance detail pages.
        - set default to hidden
- order workouts on users page based on results dates or date_completed dates on instance
        - only if there are results
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
