var infinite = new Waypoint.Infinite({
  element: $('.infinite-container')[0]
});

var dropdown = document.getElementsByClassName("dropdownOpener");

var workoutDropdowns = document.getElementsByClassName("dropdownOpenerWorkoutButtons");

function workoutDropdownFunction() {
	this.classList.toggle("active");
	var dropdownContent = this.nextElementSibling;
	if (dropdownContent.style.height == "auto") {
		dropdownContent.style.height = "0";
		dropdownContent.style.width = "0";
		dropdownContent.style.boxShadow = "none";
	} else {
		dropdownContent.style.height = "auto";
		dropdownContent.style.width = "auto";
		dropdownContent.style.boxShadow = "0 0 0 1px rgba(0,0,0,.15), 0 2px 3px rgba(0,0,0,.2)";
	}
};

var i;
for (var i = 0; i < workoutDropdowns.length; i++) {
	workoutDropdowns[i].addEventListener("click", workoutDropdownFunction, false)
}

function dropdownFunction() {
	this.classList.toggle("active");
	var dropdownContent = this.nextElementSibling;
	if (dropdownContent.style.height == "30%") {
		dropdownContent.style.height = "0";
	} else {
		dropdownContent.style.height = "30%";
	}
};

function openLeftNav() {
	document.getElementsByClassName("sidebar-nav")[0].style.overflow = "auto";
	document.getElementsByClassName("sidebar-nav")[0].style.width = "300px";
	//document.getElementsByClassName("sidebar-nav")[0].style.left = "0";
	document.getElementsByClassName("backgroundDim")[0].style.visibility = "visible";
	document.getElementsByClassName("backgroundDim")[0].style.opacity = "0.4";
	for (var i = 0; i < dropdown.length; i++) {
		dropdown[i].addEventListener("click", dropdownFunction, false) //this for loop has to be inside the openNav() function because it can't apply the on click event before the side nav has been opened. The buttons don't exist yet.
	}
}

function closeLeftNav() {
	for (var i = 0; i < dropdown.length; i++) {
		dropdown[i].nextElementSibling.style.overflow = "hidden";
		dropdown[i].nextElementSibling.style.height = "0";
	}
	document.getElementsByClassName("sidebar-nav")[0].style.overflow = "hidden";
	document.getElementsByClassName("sidebar-nav")[0].style.width = "0";
	//document.getElementsByClassName("sidebar-nav")[0].style.left = "-50px";
	document.getElementsByClassName("backgroundDim")[0].style.opacity = "0";
	document.getElementsByClassName("backgroundDim")[0].style.visibility = "hidden";	
}

function openRightNav() {
	document.getElementsByClassName("right-sidebar-nav")[0].style.overflow = "auto";
	document.getElementsByClassName("right-sidebar-nav")[0].style.width = "300px";
	document.getElementsByClassName("backgroundDim")[0].style.visibility = "visible";
	document.getElementsByClassName("backgroundDim")[0].style.opacity = "0.4";
}

function closeRightNav() {
	document.getElementsByClassName("right-sidebar-nav")[0].style.overflow = "hidden";
	document.getElementsByClassName("right-sidebar-nav")[0].style.width = "0";
	document.getElementsByClassName("backgroundDim")[0].style.opacity = "0";
	document.getElementsByClassName("backgroundDim")[0].style.visibility = "hidden";	
}

//document.getElementById("side_nav_open_button").addEventListener("click", openLeftNav, false);
document.getElementById("side_nav_open_button").addEventListener("mouseover", openLeftNav, false);
document.getElementById("side_nav_close_button").addEventListener("click", closeLeftNav, false);
document.getElementsByClassName("sidebar-nav")[0].addEventListener("mouseleave", closeLeftNav, false);

document.getElementsByClassName("notifications")[0].addEventListener("mouseover", openRightNav, false);
document.getElementById("right_sidenav_open_button").addEventListener("mouseover", openRightNav, false);
document.getElementById("right_side_nav_close_button").addEventListener("click", closeRightNav, false);
document.getElementsByClassName("right-sidebar-nav")[0].addEventListener("mouseleave", closeRightNav, false);

$(document).ready(function() {
    $('.datepicker').datepicker();
});
