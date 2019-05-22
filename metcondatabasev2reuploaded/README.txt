Edited files on 5/21/2019:
(haven't uploaded at home)
models.py
views.py
admin.py

Functionality completed on 5/21/2019:
- add duration field in results. update workoutinstance whenever results are saved to call an update_duration on instance
        - just like instance does to base workout
- change result create url to have username first, then workoutid, then result/create/
- adding a result with a new duration now updates the instance to the new duration
        - always updates instance duration to the latest results duration
- change results create view to be function based and hide instance choice and set default to the instance that was just on.
        - the function can take three args (request, user, uuid).
        - can use user and uuid for url and then use uuid for finding the instance.
        - httpresponseredirect(instance.get_absolute_url())
        - then have two inputs, one for minutes and one for seconds. use the form to validate. then use the view to transfer into only
                seconds for storing in duration field.
        - also allows files
- embed create resultfile in create result page
- display files in results
- figure out how to hide video if file is image and vis versa
        - added content_type charfield to resultfile model that checks the type of file uploaded
                - this is not great as it relies on file extension/header and can be manipulated. but its what I've got for now
                
Notes:
- work computer currently has issues displaying video. it will display fine but the command window will show errors that
        "an established connection was aborted by the software in your host machine"
        - did not occur at home so assuming this is a work only issue.
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
- increment instance number of times completed everytime a result is saved
        - possibly also add a instance completed date to instance file when result is saved?
                - could then order workouts on user page by instance completed dates
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
