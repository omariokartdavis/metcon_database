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

function addMoreStrengthMovements() {
	var form_idx = $('#id_form-TOTAL_FORMS').val();
	$('#strength_form_set').append($('#strength_workout_empty_form').html().replace(/__prefix__/g, form_idx));
	$('#id_form-TOTAL_FORMS').val(parseInt(form_idx) + 1)
}

function addMoreCardioMovements() {
	var form_idx = $('#id_form-TOTAL_FORMS').val();
	$('#cardio_form_set').append($('#cardio_workout_empty_form').html().replace(/__prefix__/g, form_idx));
	$('#id_form-TOTAL_FORMS').val(parseInt(form_idx) + 1)
}

document.getElementById("strength_add_more").addEventListener("click", addMoreStrengthMovements, false);
document.getElementById("cardio_add_more").addEventListener("click", addMoreCardioMovements, false);
