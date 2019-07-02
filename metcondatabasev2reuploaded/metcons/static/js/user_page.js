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
  
  $('html, body').animate({ scrollTop: 0 }, 'fast');
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
  var athletes = document.getElementsByClassName("athleteButton");
  for (i = 0; i < athletes.length; i++) {
    athletes[i].className = athletes[i].className.replace(" active", "");
  } 
  document.getElementById("chosenAthlete").value = athleteUsername;
  document.getElementById("whichUserDisplay").submit();
}

var athleteButtons = document.getElementsByClassName("athleteButton");
if (athleteButtons) {
  for (i = 0; i < athleteButtons.length; i++) {
    athleteButtons[i].addEventListener("click", queryAthlete, false);
  }
}

window.onload = document.getElementById("defaultOpenTab").click();

window.onload = function() {
  var url_string = window.location.href;
  var url = new URL(url_string);
  var q = url.searchParams.get("q");
  if (q) {
	document.getElementById(q).className += " active";
  } else {
	document.getElementsByClassName("defaultOpenUser")[0].className += " active";
	document.getElementsByClassName("defaultOpenUser")[0].click();
  }
}

var lastScrollTop = 0;
$(window).scroll(function(){
	var st = $(this).scrollTop();
	var tablinks = document.getElementsByClassName("tablinks"), i, tablink, specificTabLink;
	for (i = 0; i < tablinks.length; i++) {
		tablink = tablinks[i];
		if ($(tablink).hasClass('active')) {
			specificTabLink = tablink;
		}
	}
	var specificTabLinkStartPosition = specificTabLink.style.left;
	if (st > lastScrollTop){
		$(".tab button:not(#" + specificTabLink.id + ")").css("opacity", 0);
		$(".tab button:not(#" + specificTabLink.id + ")").css("visibility", "hidden");
		//$(".tab").css("width", 100);
		//$(".tab").css("left", 200);
	} else {
		//$(".tab").css("left", 100);
		//$(".tab").css("width", 400);
		//$(".tab button:not(#tabID)").fadeIn( "fast");
		$(".tab button:not(#" + specificTabLink.id + ")").css("visibility", "visible");
		$(".tab button:not(#" + specificTabLink.id + ")").css("opacity", 0 + ($(window).scrollTop()  + $(window).height()) / 50);
	}
	lastScrollTop = st;
	if ($(window).scrollTop() >= 150) {
		$(".somediv").css("top", 0);
		$(".tab").css("top", 260);
		$(".athleteTab").css("top", 260);
		$(".athletesNames").css("top", 310);
	} else {
		$(".somediv").css("top", 150 - $(window).scrollTop());
		$(".tab").css("top", 410 - $(window).scrollTop());
		$(".athleteTab").css("top", 410 - $(window).scrollTop());
		$(".athletesNames").css("top", 460 - $(window).scrollTop());
	}
});
