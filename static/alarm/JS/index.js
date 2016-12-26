var data = JSON.parse(json_string);

var now = data.now_str;
var now_mon = data.now_month;

function days(time_string) {
  var day = time_string.substring(3, 5);
  return Number(day)
}

function hours(time_string) {
  var hour = time_string.substring(9, 11);
  return Number(hour);
  }

function minutes(time_string) {
  var minute = time_string.substring(12, 14);
  return Number(minute);
  }

function seconds(time_string) {
  var second = time_string.substring(15, 17);
  return Number(second);
  }

// TODO: Learn about arrays and improve the function month

function month(now_mon) {
	if(now_mon==1){
		return "Jan"
	}
	if(now_mon==2){
		return "Feb"
	}
	if(now_mon==3){
		return "March"
	}
	if(now_mon==4){
		return "April"
	}
	if(now_mon==5){
		return "May"
	}
	if(now_mon==6){
		return "June"
	}
	if(now_mon==7){
		return "July"
	}
	if(now_mon==8){
		return "Aug"
	}
	if(now_mon==9){
		return "Sep"
	}
	if(now_mon==10){
		return "Oct"
	}
	if(now_mon==11){
		return "Nov"
	}
	if(now_mon==12){
		return "Dec"
	}
}

function increase(seconds, minutes, hours, days, id_sec, id_min, id_hour, id_day){
	var total_seconds = seconds;
	var total_minutes = minutes;
	var total_hours = hours;
	var total_days = days;
	function inc() {
		total_seconds = total_seconds + 1;
		seconds = total_seconds % 60;
		document.getElementById(id_sec).innerHTML = seconds;
		
		if(seconds == 0){
			total_minutes = total_minutes + 1;
			document.getElementById(id_min).innerHTML = total_minutes%60;
		}
		if(total_minutes%60 == 0 && seconds == 0){
			total_hours = total_hours + 1;
			document.getElementById(id_hour).innerHTML = total_hours%24;
		}
		if(total_hours%24==0 && total_minutes%60 == 0 && seconds == 0){
			total_days = total_days + 1;
			document.getElementById(id_day).innerHTML = total_days%31;
		}
	}
	var timeinterval = setInterval(inc, 1000);
}

// Store time in it's components:
var now_day = days(now);

var now_hr = hours(now);

var now_min = minutes(now);

var now_sec = seconds(now);

var month_str = month(now_mon);

increase(now_sec, now_min, now_hr, now_day, 'now_seconds', 'now_minutes', 'now_hours', 'now_days');

document.getElementById('now_days').innerHTML = now_day;
document.getElementById('now_hours').innerHTML = now_hr;
document.getElementById('now_minutes').innerHTML = now_min;
document.getElementById('now_seconds').innerHTML = now_sec;
document.getElementById('now_month').innerHTML = month_str;

var modal = document.getElementById('myModal');

// Get the button that opens the modal
var btn_time = document.getElementById("open_modal_time");
var btn_duration = document.getElementById("open_modal_duration");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal 
btn_time.onclick = function(){
	modal.style.display = "block";
};

btn_duration.onclick = function(){
	modal.style.display = "block";
};

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

var sbmt_btn = document.getElementById("submit_main_form");
var time_form = document.getElementsByClassName("time_form");
var duration_form = document.getElementById("duration_form");

sbmt_btn.onclick = function() {
	message = document.getElementById("message").value;
	try{
		document.getElementById("main_message_time").value = message;
		time_form.submit();
	}
	catch(err){
		document.getElementById("main_message_duration").value = message;
		duration_form.submit();
	}
}