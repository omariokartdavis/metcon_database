$(document).ready(function() {
	$('#workout_type_selector').on('change', function() {
		var i, all_forms;
		all_forms = document.getElementsByClassName("workout_form")
		for (i = 0; i < all_forms.length; i++) {
			all_forms[i].style.display = "none";
		}
		var target_form = document.getElementById(this.value);
		target_form.style.display = "block";
	});
});