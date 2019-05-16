Edited files on 5/16/2019:
workoutinstance_detail.html (uploaded at work)
workout_list.html (uploaded at work)
views.py (uploaded at work)
urls.py (uploaded at work)
workout_detail.html (uploaded at work)
base_generic.html (uploaded at work)
models.py (uploaded at work) (requires makemigrations/migrate, doesn't required database reset)
user_page.html (uploaded at work)

Functionality completed on 5/16/2019:
- if user isn't logged in, workout list page only shows 10 most recent workouts by date created
- change duration search to be gt=0 instead of gte=1
- date added to profile in workoutinstance_detail now works properly
- change home button to not hide if user isn't authenticated but instead takes them to the index page or login page
- added Add Workout button on workout_detail page.
        - required changing detail view from a class based view to function based view.
        - likely have to do the same to allow on workout_list view.
        - the base render(request, 'page_link') page_link must be = 'metcons/template_name.html'
        - have to change urls.py as well from class based view to function view
- added sort by popularity checkbox
- changed foreignkey models to on_delete=null in workout and workoutinstance
- when creating a new workout, create a new instance as well for that user
        - creating a workout now sends you to your instance page after workout creation. not the workout detail page itself.

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
- only allow user who created base workout in database to edit that workout and only while no one else has added it to their page
        - if edited after others have it on their profile, it will change everyones workout.
- add user field of "sport" and they can choose between crossfit, bodybuilding, strength training etc.
        - their choice here will determine their views and workout types shown
- once the above is added, add ability to switch workout_list searches to different sport types
        - if an athlete's sport is BB give a dropdown that allows them to switch to Crossfit workouts or other.
- add click to edit button on workout instance detail page.
        - only edit fields specific to that instance aka duration completed, times completed, dates completed etc.
        - may require an update view
- get rid of pagination on workout list if not logged in but keep it if logged in.
        - just adding block pagination endblock gets rid of pagination in both situations
        - this will likely solve itself when endless scroll is added
- login url is currently metcons/profile instead of metcons/<username> not sure how to fix this as redirect doesn't seem to be working
- add login to index page.
- add results section to bottom of workoutinstance detail page for users to add resultsk
- can use .aggregate(AVG) for estimated duration which will average all durations of instances and put them into
        the base workout. This way as more users complete a workout the duration gets updated.
        - should work just like SUM of times completed
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
