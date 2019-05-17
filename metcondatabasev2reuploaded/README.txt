Edited files on 5/17/2019:
views.py (haven't uploaded at work)
urls.py (haven't uploaded at work)
workout_list.html (haven't uploaded at work)
workout_detail.html (haven't uploaded at work)

Functionality completed on 5/17/2019:
- added an if function on workoutdetailview add workout to profile button
        - if instance already exists for user, go to that instance page. Otherwise create instance and go.
- changed workoutlistview to function view and added add workout to profile button
- added user authentication check to workout detail

Notes:
- can't use onetoone between user and workoutinstance because then they can't have multiple workouts. has to be foreign key and create
        some restriction where if the workoutinstance with that specific workout already exists for that user it just pulls that up.
        this will likely have to be handled in the views.py
- to allow urls to extend with info, the get_absolute_url function must be in the model isntance and you must pass the arguments
        for each specification before it. otherwise you will get a reverse match not found on the template link.
        - see workout instance get_absolute_url for example
        - if using function based views, the argument must also be passed in the view function
                - see profile view as example
                - class based views take this into account with the models get_aboslute_url
        
Functionality to add:
- ?add user authentication check to movements list?
- change date added/created fields on all models to datetime fields to allow for most accurate tracking
        - will require reset of database and changing of mainsite_workouts to put datetime instead of just date.
        - will also likely require change of movements_list instance completed dates.
- only allow user who created base workout in database to edit that workout and only while no one else has added it to their page
        - if edited after others have it on their profile, it will change everyones workout.
- add user field of "sport" and they can choose between crossfit, bodybuilding, strength training etc.
        - their choice here will determine their views and workout types shown
- once the above is added, add ability to switch workout_list searches to different sport types
        - if an athlete's sport is BB give a dropdown that allows them to switch to Crossfit workouts or other.
- add click to edit button on workout instance detail page.
        - only edit fields specific to that instance aka duration completed, times completed, dates completed etc.
        - may require an update view
- Pagination:
        - add pagination to workout list and profile page.
                - workout list pagination got removed becuase I changed it to a function view to allow POST forms
        - get rid of pagination on workout list if not logged in but keep it if logged in.
                - just adding block pagination endblock gets rid of pagination in both situations
        - this will likely solve itself when endless scroll is added
- login url is currently metcons/profile instead of metcons/<username> not sure how to fix this as redirect doesn't seem to be working
- add login to index page.
- add results section to bottom of workoutinstance detail page for users to add resultsk
- can use .aggregate(AVG) for estimated duration which will average all durations of instances and put them into
        the base workout. This way as more users complete a workout the duration gets updated.
        - should work just like SUM of times completed
        - can use .filter(duration_gt=0).aggregate(AVG()) to exclude instances where duration hasn't been changed
- add results model and foreign key it to workoutinstance to store peoples results of their workouts (weights, videos, description of difficulty)
        - time workout completed in can still be stored in instances duration.
        - date of results and a textfield will be important.
        - ?allow for pictures and videos how?
        - on users workout detail view of their own instance, show results underneath ordered by most recently completed
- ?Make movement tags only match full movement name?
        - could probably find a way that after movements are added, create list of movements names. search through list for a specific
                movement name and if it appears twice (Clean, Clean and Jerk) remove the movement (clean gets removed).
        - not sure if this is a good idea on second thought as this would mean workouts with Power Snatch are no longer tagged
                as Snatch. may be better to just leave as is.
- Add search for a specific users workouts
        - search for workouts mat fraser has done
        - filter for workouts whose workout instances have users of xx name
                - maybe this is a subquery?
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
