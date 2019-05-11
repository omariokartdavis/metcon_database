Edited files on 5/11/2019:
workouts_list.html (haven't reuploaded)
views.py (haven't reuploaded)
models.py (haven't reuploaded)
admin.py (haven't reuploaded)
mainsite_workouts.py (no)
movements_list.py (no)

Functionality completed on 5/11/2019:
- multiple search boxes for movements added
- populate search box with chosen filters
- don't hide dropdown when reclicking in search box. only hide on clicking out of all search boxes
- added workout instance model
- added workout instance completed dates model
- added workout instance count to workout model
        - also displayed on admin page
        
Functionality to add:
- make one dropdown close if you click on the other
        - likely have to make all dropdowns a different class for this to work.
- consolidate javascript code on workouts_list.html
- Endless Scroll of workouts
- ?Make movement tags match movement names by regex full match?
        - don't think this will help as 'Squat Snatch' will still regex as 'Squat' and 'Snatch'
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
- Add filters currently active below search boxes after a filter is chosen
- Add back button to previous search after filtering
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

