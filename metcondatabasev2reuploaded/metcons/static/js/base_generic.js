function openNav() {
	document.getElementsByClassName("sidebar-nav")[0].style.width = "300px";
	document.getElementsByClassName("sidebar-nav")[0].style.left = "0";
	//document.body.style.backgroundColor = "rgba(0,0,0,0.4)";
	document.getElementsByClassName("backgroundDim")[0].style.visibility = "visible";
	document.getElementsByClassName("backgroundDim")[0].style.opacity = "0.4";
}

function closeNav() {
	document.getElementsByClassName("sidebar-nav")[0].style.width = "0";
	document.getElementsByClassName("sidebar-nav")[0].style.left = "-50px";
	document.getElementsByClassName("backgroundDim")[0].style.opacity = "0";
	document.getElementsByClassName("backgroundDim")[0].style.visibility = "hidden";	
}

document.getElementById("side_nav_open_button").addEventListener("click", openNav, false);
document.getElementById("side_nav_close_button").addEventListener("click", closeNav, false);