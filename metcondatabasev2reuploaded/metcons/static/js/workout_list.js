function Dropdown() {
  //this event is only on the textinput boxes so I can't close dropdowns when the submit button is focused.
  //using onblur makes the setDropdown Selection function not work because the moment you click out of the text input the dropdown disappears. making it as if you didnt
  // click a selection in the dropdown.
  // add an onfocus for the submit button to close all dropdowns is simplest way to avoid dropdowns staying up when tabbing through elements.
  // can't add onfocus for the sidebar nav so shift tabbing back to nav from first input box leaves dropdown up currently.
  var dropdowns = document.getElementsByClassName("dropdown-content");
  var i;
  for (i = 0; i < dropdowns.length; i++) {
    if (dropdowns[i] != this.nextSibling.nextSibling) {
	  if (dropdowns[i].classList.contains("show")) {
	    dropdowns[i].classList.remove("show");
	  }
	}
  }
  this.nextSibling.nextSibling.classList.add("show");
}

function DropdownExit() {
  var dropdowns = document.getElementsByClassName("dropdown-content");
  var i;
  for (i = 0; i < dropdowns.length; i++) {
	if (dropdowns[i].classList.contains("show")) {
	  dropdowns[i].classList.remove("show");
	}
  }
}

function Filter() {
  var input, filter, ul, li, option, i;
  input = this;
  filter = this.value.toUpperCase();
  div = input.nextSibling.nextSibling;
  option = div.getElementsByTagName("option");
  for (i = 0; i < option.length; i++) {
    txtValue = option[i].textContent || option[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      option[i].style.display = "";
    } else {
      option[i].style.display = "none";
    }
  }
}

function setDropdownSelection() {
  var selectedOption = this.options[this.selectedIndex];
  var textValue = selectedOption.text;
  var textBox = this.parentNode.previousSibling.previousSibling;
  textBox.value = textValue;
}

var textinputs = document.getElementsByClassName("textinput");
var i;
if (textinputs) {
  for (i = 0; i < textinputs.length; i++) {
    textinputs[i].addEventListener("focus", Dropdown, false);
	textinputs[i].addEventListener("keyup", Filter, false);
  }
}
var durationinputs = document.getElementsByClassName("durationinput");
var i;
if (durationinputs) {
  for (i = 0; i < durationinputs.length; i++) {
    durationinputs[i].addEventListener("focus", DropdownExit, false);
  }
}

var dropdownselects = document.getElementsByClassName("dropdown-selection");
if (dropdownselects) {
  for (i = 0; i < dropdownselects.length; i++) {
    dropdownselects[i].addEventListener("change", setDropdownSelection, false);
  }
}

var filterSubmitButton = document.getElementById("filtersubmitbutton");
if (filterSubmitButton) {
  filterSubmitButton.addEventListener('focus', DropdownExit, false);
}

window.onclick = function(event) {
  //use console.log(event) and possibly event.nextSibling etc. to see what element is being triggered by clicking on things.
  var dropdowns = document.getElementsByClassName("dropdown-content");
  var i;
  if (!event.target.matches('.textinput')) {
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }   
}
