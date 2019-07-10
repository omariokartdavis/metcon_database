var dropdown = document.getElementsByClassName("dropdownOpener");

function dropdownFunction() {
	this.classList.toggle("active");
	var dropdownContent = this.nextElementSibling;
	if (dropdownContent.style.height == "60%") {
		dropdownContent.style.height = "0";
	} else {
		dropdownContent.style.height = "60%";
	}
};

function openNav() {
	document.getElementsByClassName("sidebar-nav")[0].style.width = "300px";
	document.getElementsByClassName("sidebar-nav")[0].style.left = "0";
	//document.body.style.backgroundColor = "rgba(0,0,0,0.4)";
	document.getElementsByClassName("backgroundDim")[0].style.visibility = "visible";
	document.getElementsByClassName("backgroundDim")[0].style.opacity = "0.4";
	for (var i = 0; i < dropdown.length; i++) {
		dropdown[i].addEventListener("click", dropdownFunction, false) //this for loop has to be inside the openNav() function because it can't apply the on click event before the side nav has been opened. The buttons don't exist yet.
	}
}

function closeNav() {
	document.getElementsByClassName("sidebar-nav")[0].style.width = "0";
	document.getElementsByClassName("sidebar-nav")[0].style.left = "-50px";
	document.getElementsByClassName("backgroundDim")[0].style.opacity = "0";
	document.getElementsByClassName("backgroundDim")[0].style.visibility = "hidden";	
}

document.getElementById("side_nav_open_button").addEventListener("click", openNav, false);
document.getElementById("side_nav_close_button").addEventListener("click", closeNav, false);
