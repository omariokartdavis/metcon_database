Edited files on 5/16/2019:
workoutinstance_detail.html (haven't uploaded at work)
workout_list.html (haven't uploaded at work)
views.py (haven't uploaded at work)


Functionality completed on 5/15/2019:
- if user isn't logged in, workout list page only shows 10 most recent workouts by date created
        still has pagination though
- change duration search to be gt=0 instead of gte=1
- date added to profile in workoutinstance_detail now works properly
Last working on:
- add workout to profile button on workout list. need form submit but may need multiple forms on that page.

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
- get rid of pagination on workout list if not logged in but keep it if logged in.
        - just adding block pagination endblock gets rid of pagination in both situations
- login url is currently metcons/profile instead of metcons/<username> not sure how to fix this as redirect doesn't seem to be working
- change home button to not hide if user isn't authenticated but instead takes them to the index page or login page
- add results section to bottom of workoutinstance detail page for users to add results
- workouts list page can have a if user.is_authenticated to show all workouts if the user is logged in
        and if they aren't then only show the 10 most recent workouts completed
- when creating a new workout, create a new instance as well for that user
        - workout(info), workout.save(), workoutInstance(info), workoutInstance.save()
- can use .aggregate(AVG) for estimated duration which will average all durations of instances and put them into
        the base workout. This way as more users complete a workout the duration gets updated.
        - should work just like SUM of times completed
- add workout to a users page
        - would be a form on the workout_detail.html page
                - likely going to be a post form that when clicked creates a workout instance for that user. No info should be needed
                        all info can come directly from the workout and just add user tag to the instance.
                        use self.request.user to get the current user in the workout list view
        - could also be a link next to the workout on the workout_list.html page
        - Creation has to be done in views.py
        - creates an instance for that specific user with no completed dates. 
                can then ask if they have already completed this workout and would like to log when and what their time/performance was
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
- Add filter for popularity of workout.
        - would simply change ordering to order by number of times completed or number of instances created.
        - Workout.objects.order_by('number_of_times_completed') or 'number_of_instances'
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
