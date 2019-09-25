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
	var openCreateMovementButtons = document.getElementsByClassName("open_create_movement_button")

	var i;
	for (var i = 0; i < openCreateMovementButtons.length; i++) {
		openCreateMovementButtons[i].addEventListener("click", openCreateMovementPopup, false)
	}
}

function addMoreCardioMovements() {
	var form_idx = $('#cardio_id_form-TOTAL_FORMS').val();
	$('#cardio_form_set').append($('#cardio_workout_empty_form').html().replace(/__prefix__/g, form_idx));
	$('#cardio_id_form-TOTAL_FORMS').val(parseInt(form_idx) + 1)
}

function openCreateMovementPopup() {
	document.getElementsByClassName("backgroundDim")[0].style.visibility = "visible";
	document.getElementsByClassName("backgroundDim")[0].style.opacity = "0.4";
	document.getElementsByClassName("popup")[0].style.visibility = "visible";
	document.getElementsByClassName("popup")[0].style.opacity = "1";
	document.getElementsByClassName("popup2")[0].style.visibility = "visible";
	document.getElementsByClassName("popup2")[0].style.opacity = "1";
}

function closeCreateMovementPopup() {
	document.getElementsByClassName("backgroundDim")[0].style.opacity = "0";
	document.getElementsByClassName("backgroundDim")[0].style.visibility = "hidden";
	document.getElementsByClassName("popup")[0].style.opacity = "0";
	document.getElementsByClassName("popup")[0].style.visibility = "hidden";
	document.getElementsByClassName("popup2")[0].style.opacity = "0";
	document.getElementsByClassName("popup2")[0].style.visibility = "hidden";
}

var openCreateMovementButtons = document.getElementsByClassName("open_create_movement_button")

var i;
for (var i = 0; i < openCreateMovementButtons.length; i++) {
	openCreateMovementButtons[i].addEventListener("click", openCreateMovementPopup, false)
}

var closeCreateMovementButtons = document.getElementsByClassName("close_create_movement_button")

var i;
for (var i = 0; i < closeCreateMovementButtons.length; i++) {
	closeCreateMovementButtons[i].addEventListener("click", closeCreateMovementPopup, false)
}

document.getElementById("strength_add_more").addEventListener("click", addMoreStrengthMovements, false);
document.getElementById("cardio_add_more").addEventListener("click", addMoreCardioMovements, false);
