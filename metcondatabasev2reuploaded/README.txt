Edited files on 5/14/2019:
models.py (uploaded at home)
view.py (uploaded at home)
workout_list.html (uploaded at home)
metcondatabasev2reuploaded/metcondatabasev2/urls.py (uploaded at home)
metcondatabasev2reuploaded/metcondatabasev2/settings.py (uploaded at home)
created projectroot/templates/registration (uploaded at home)

Functionality completed on 5/14/2019:
- add_date_completed for WorkoutInstance works
- refresh page on update Workout button click on workout_detail page
- increment_number_of_times_completed in WorkoutInstance works and is proper
- update_number_of_times_completed in Workout works and is proper
- Add filter for duration of workout
- create some user accounts and login page

Notes:
- can't use onetoone between user and workoutinstance because then they can't have multiple workouts. has to be foreign key and create
        some restriction where if the workoutinstance with that specific workout already exists for that user it just pulls that up.
        this will likely have to be handled in the views.py
        
Functionality to add:
- regex search for "as many rounds as possible in xx minutes of:" could add duration to amrap workouts from mainsite
- add workout to a users page
        - would be a form on the workout_detail.html page
        - could also be a link next to the workout on the workout_list.html page
        - Creation has to be done in views.py
        - creates an instance for that specific user with no completed dates. 
                can then ask if they have already completed this workout and would like to log when and what their time/performance was
- add results textfield to workoutinstance to store peoples results of their workouts (weights, videos, description of difficulty)
        - time workout completed in can still be stored in instances duration.
- ?Make movement tags only match full movement name?
        - could probably find a way that after movements are added, create list of movements names. search through list for a specific
                movement name and if it appears twice (Clean, Clean and Jerk) remove the movement (clean gets removed).
        - not sure if this is a good idea on second thought as this would mean workouts with Power Snatch are no longer tagged
                as Snatch. may be better to just leave as is.
- Add filter for popularity of workout.
        - would simply change ordering to order by number of times completed or number of instances created.
- Add search for a specific users workouts
        - search for workouts mat fraser has done
        - filter for workouts whose workout instances have users of xx name
                - maybe this is a subquery?
- Create a user homepage (accounts/profile/)
- Combine Create Movement and Update Workout buttons into a popup:
        -on create movement button click open a popup to add movement. on save click run three functions:
                -save movement
                -update current workout
                -refresh page
- Come up with a better way to list workouts instead of by workout number
        -add name to workout model or workoutinstance model and allow for blank/null. If name exists list by name otherwise list
                by "workout " + str(id)
        -would also change def __str__ to if statement on if name exists otherwise same as above
- Add abbreviations to some movements?
        could change movement_list to a list of lists:
        movement_list = [
                ['Pull Up', 'Upper Body', ['abbrvs']],...]
         then in the for loop just use:
         for i in all_movements:
                for x, y, z in i:
                        movement = Movement(name=x,
                                        classification = Classification.objects.get(name=y),
                                        abbreviations = [a for a in z]

Styling:
- Create stylebook for all screens
- Create table for viewing workouts
        similar to the styling of this: https://fooplugins.github.io/FooTable/docs/examples/advanced/filter-dropdown.html
- Endless Scroll of workouts
- Add back button to previous search after filtering
- Add filters currently active below search boxes after a filter is chosen
