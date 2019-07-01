function openTab(evt) {
  // Declare all variables
  var i, tabcontent, tablinks, tabName;
  tabName = evt.target.firstChild.nodeValue

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(tabName).style.display = "block";
  evt.currentTarget.className += " active";
}

var tabs = document.getElementsByClassName("tablinks");
var i;
if (tabs) {
  for (i = 0; i < tabs.length; i++) {
    tabs[i].addEventListener("click", openTab, false);
  }
}


function queryAthlete(evt) {
  var i, athleteUsername;
  
  athleteUsername = evt.target.firstChild.nodeValue;
  console.log(athleteUsername);
  document.getElementById("chosenAthlete").value = athleteUsername;
  document.getElementById("whichUserDisplay").submit();
}

var athleteButtons = document.getElementsByClassName("athleteButton");
if (athleteButtons) {
  for (i = 0; i < athleteButtons.length; i++) {
    athleteButtons[i].addEventListener("click", queryAthlete, false);
  }
}
const NAME = "once";

window.onload = document.getElementById("defaultOpenTab").click();
window.onload = function defaultToUser() {
	if (this.name !== NAME) {
		this.name = NAME;
		document.getElementById("defaultOpenUser").click();
		splashScreen();
	} else {
		console.log(this.name)
	}
}