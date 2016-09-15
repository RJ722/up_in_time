var data = JSON.parse(json_string);

var now = data.now_str;
var alarm_time = data.alarm_time;


document.getElementById("datetime").innerHTML = "Now: " + data.now_str + "<br>" +
												                        "Alarm Time: " + data.alarm_time;

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

// Store time in it's components:
var now_day = days(now);
var alarm_day = days(alarm_time);

var now_hr = hours(now);
var alarm_hr = hours(alarm_time);

var now_min = minutes(now);
var alarm_min = minutes(alarm_time);

var now_sec = seconds(now);
var alarm_sec = 0;

function getTimeDiff(now, alarm_time) {

  var seconds = alarm_sec - now_sec;
  var minutes = alarm_min - now_min;
  var hours = alarm_hr - now_hr;
  var days = alarm_day - now_day;
  var total = days*24*60*60 + hours * 60 * 60 + minutes * 60 + seconds;

  return {
    'total': total,
    'days' : days,
    'hours': hours,
    'minutes': minutes,
    'seconds': seconds
  };
}

function initializeClock(now, alarm_time, callback, callback_param) {
  function updateClock() {
    var t = getTimeDiff(now, alarm_time);
    now_sec = now_sec + 1
    console.log(now_sec);
    console.log(t);
    if (t.total <= 0) {
      clearInterval(timeinterval);
      callback(callback_param);
    }
  }

  updateClock();
  var timeinterval = setInterval(updateClock, 1000);
}

function call_alert(message) { 
  window.alert(message)
}

var message = "Bhai Alarm Time ho gya hai UtHO BC"

initializeClock(now, alarm_time, call_alert, message);

