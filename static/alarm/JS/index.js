function display_c(){
	var refresh=1000; // Refresh rate in milli seconds
	mytime=setTimeout('display_ct()',refresh);
}

function display_ct() {
	console.log("display_ct is now being executed!")
	var strcount;
	var x = new Date();
	document.getElementById('ct').innerHTML = x;
	tt=display_c();
}

document.addEventListener('DOMContentLoaded', function() {
    display_ct();
}, false);

var my_modal_time = document.getElementById("message_modal_time");
var my_modal_duration = document.getElementById("message_modal_duration");

// Get the button that opens the modal
var btn_time = document.getElementById("open_modal_time");
var btn_duration = document.getElementById("open_modal_duration");

// When the user clicks the button, open the modal 
btn_time.onclick = function(){
	my_modal_time.style.display = "block";
	$('#message_time').focus();
	$(document).keyup(function(e) {
		if (e.keyCode === 13) {
			$('#submit_time_form').click();
	}
});
};

btn_duration.onclick = function(){
	my_modal_duration.style.display = "block";
	$('#message_duration').focus();
	$(document).keyup(function(e) {
		if (e.keyCode === 13) {
			$('#submit_duration_form').click();
	}
});
}

$(document).keyup(function(e) {
		if (e.keyCode === 27) {
			$('#message_modal_duration').css("display", "none");
			$('#message_modal_time').css("display", "none");

	}
});

// When the user clicks on <span> (x), close the modal
$('.close').click(function() {
    my_modal_time.style.display = "none";
    my_modal_duration.style.display = "none";
});

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == my_modal_time) {
        my_modal_time.style.display = "none";
    }
    if (event.target == my_modal_duration){
    	my_modal_duration.style.display = "none";
    }
}

// Get the button on the modak which then submits the required form.
var sbmt_btn_time = document.getElementById("submit_time_form");
var sbmt_btn_duration = document.getElementById("submit_duration_form");

// Get both of the forms on the page.
var time_form = document.getElementById("time_form");
var duration_form = document.getElementById("duration_form");

sbmt_btn_time.onclick = function() {
	message = document.getElementById("message_time").value;
	document.getElementById("main_message_time").value = message;
	time_form.submit();
	console.log("Time form is submitted!")
	}

sbmt_btn_duration.onclick = function() {
	message = document.getElementById("message_duration").value;
	document.getElementById("main_message_duration").value = message;
	console.log("Original message: " + message);
	console.log("After copying: " + document.getElementById("main_message_duration").value)
	duration_form.submit();
	console.log("Duration form is submited");
}
