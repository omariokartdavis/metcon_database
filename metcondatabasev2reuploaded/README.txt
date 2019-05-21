Edited files on 5/20/2019:
models.py (haven't uploaded at home) requires deleting and readding workouts and instances only
views.py
forms.py
mainsite_workouts.py
admin.py
urls.py
workout_detail
workoutinstance_detail
result_form.html

Functionality completed on 5/20/2019:
- .aggregate(AVG()) to update workout duration upon adding instances.
        - not sure if this is a good idea but it is done
- change (if complete as many rounds as possible) to be faster:
        - changed it from a regex search on workout_text to a filter for workouts with workout.id and iregex text
- changed workout_detail and instance_detail to show date created as date only not date and time.
        - only need time for ordering purposes
- added results model
- added resultsfile model to handle pictures/videos
- changed duration to seconds on all models
        - all views have been updated except for resultcreate view
- added list of results underneath workoutinstance description
- undid workoutdetail.date and instance.date because its rounding dates forward to the next day.


Notes:
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
- have to embed in the result create page, the resultfiles create
- order workouts on users page based on results dates or date_completed dates on instance
- add filter on workout instance detail page to filter results by date
- ?put filter searches on base_generic page and do {% block filters %}{% endblock %} if you don't want them to come up?
- need to list workouts on user_page by dates completed not just added to user date.
        - maybe only by dates completed if there is one?
- only allow user who created base workout in database to edit that workout and only while no one else has added it to their page
        - if edited after others have it on their profile, it will change everyones workout.
- add user field and workout field of "sport" and they can choose between crossfit, bodybuilding, strength training etc.
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
- add login to index page.
- add results section to bottom of workoutinstance detail page for users to add resultsk
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
- Add privacy setting so users can set their profile/workouts to private and therefore others can search for/see them.
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
