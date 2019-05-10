Edited files on 5/10/2019:
Don't forget to createsuperuser if deleting the database
movements_list.py (includes core and classifications update. May need to reset database for this)
mainsite_workouts.py
Created update_all_workout_movement_and_class_tags.py
workout_list.html
views.py
models.py

Functionality completed on 5/10/2019:
- Create search and filter for workouts based on movements and classifications
        - not including fully case insentive search. Can search for exact match or title case only.
        - including multiple movement search.
        - related links:
                https://www.w3schools.com/howto/howto_js_filter_dropdown.asp
                https://www.w3schools.com/howto/howto_js_filter_lists.asp
                https://fooplugins.github.io/FooTable/docs/examples/advanced/filter-dropdown.html
- Dropdowns now close when clicking out of all search boxes
- Allow for database updating of movement tags for all workouts at once when a new movement is added

Functionality to add:
- make one dropdown close if you click on the other
        - on work computer script.js should have functionality for turning display to show but not back to hide
- Endless Scroll of workouts
- ?Make movement tags match movement names by regex full match?
        - don't think this will help as 'Squat Snatch' will still regex as 'Squat' and 'Snatch'
- Add workout instance for users
        - helpful info from bookinstance model here: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Models
- change number of times completed in base workout model to add together all times that workout was completed from all instances
        - ?keep count variable and create a method that updates that count variable based on all count variables in instances?
                - ?maybe only calls update when an instance is updated?
                - ?maybe only called once a night overnight?
- change number of times completed in instance to be specific to that instance
        - ?keep count variable and create a method that updates the count variable whenever a box is checked?
- Add search and filter for popularity of workout.
        - only possible after adding count variables for base workout and workoutinstance
- Create a user homepage
- Create user accounts and login page
- Change create movement page to a popup page when link is clicked (this should allow for on page adding and refreshing of movements)
- Allow for on page refreshing of movement tags/classifications
        -should be doable with javascript to refresh page after updating.
        -on create movement button click open a popup to add movement. on save click run three functions:
                -save movement
                -update current workout
                -refresh page
- Come up with a better way to list workouts instead of by workout number
        -add name to workout model or workoutinstance model and allow for blank/null. If name exists list by name otherwise list
                by "workout " + str(id)
        -would also change def __str__ to if statement on if name exists otherwise same as above
- Add search and filter functionality for duration of workout
        -requires adding range functionality
- Populate search box with chosen filters
- Add filters currently active below search boxes after a filter is chosen
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

