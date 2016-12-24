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
	var total_seconds = 0;
	var total_minutes = 0;
	var total_hours = 0;
	var total_days = 0;
	function inc() {
		if(seconds < 59){
			seconds = seconds + 1;
			total_seconds = total_seconds + 1;
			document.getElementById(id_sec).innerHTML = seconds;
		}
		if(seconds >= 59){
			minutes = minutes + 1;
			document.getElementById(id_min).innerHTML = minutes;
			seconds = 0;
		}
		if(total_seconds >= 3600){
			hours = hours + 1;
			document.getElementById(id_hour).innerHTML = hours;
			minutes = 0;
		}
		if(total_seconds > 24*3600){
			days = days + 1;
			document.getElementById(id_day).innerHTML = days;
			hours = 0;
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

