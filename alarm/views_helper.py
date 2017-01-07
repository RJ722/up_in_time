import datetime
import unicodedata
import webbrowser
import time
import pytz

from django.shortcuts import render, redirect
from alarm.models     import Alarm
from django.utils     import timezone
from django.utils.timezone import localtime

def check_alarm_time(alarm_time):
	"""
	Checks if the alarm_time is in future.
	"""
	# Consider alarm_time is a datetime object.
	now = timezone.now()
	if not alarm_time > now:
		return False
	return True

def check(request, alarm_time, s_dict, errors):
	"""
	A wrapper around check_alarm_time.
	"""
	if not check_alarm_time(alarm_time):
		error = "Please enter a future Time"
		errors.append(error)
		s_dict["errors"].append(error)
		return s_dict

def uni_to_str(uni):
	"""
	Converts the given unicode string to a pythonic one.
	"""
	return unicodedata.normalize('NFKD', uni).encode('ascii','ignore')

def get_alarm_time_from_duration(duration):
	"""
	Rteurns a tuple of alarm_hours and alarm_minutes when duration (string) is given.
	"""
	try:
		alarm_hours = int(duration[:2])
		alarm_minutes = int(duration[3:])
	except:
		alarm_hours = 0
		alarm_minutes = 0
	return (alarm_hours, alarm_minutes)

def get_client_ip(request):
	"""
	Returns client IP
	"""
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip

def check_and_save(request, alarm_time):
	"""
	For a particular IP, writes the given alarm_time in the database.
	Updates the time if time already present.
	"""
	ip = get_client_ip(request)
	current_alarm = None
	# Extract message (already in str format)
	message = request.POST.get("main_message", "")

	for alarm in Alarm.objects.all():
		if ip == alarm.ip_address:
			current_alarm = alarm
			break

	if current_alarm == None:
		current_alarm = Alarm(alarm_time=alarm_time, ip_address=ip, message = message)
	else:
		current_alarm.alarm_time = alarm_time
		current_alarm.message = message 
		
	current_alarm.save()

def convert_to_utc(alarm_time):
	"""
	Takes naive alarm_time in local timezone format and converts to UTC aware alarm_time.
	"""
	local = timezone.get_current_timezone()
	local_dt = local.localize(alarm_time, is_dst=None)
	utc_dt = local_dt.astimezone(pytz.utc)
	return utc_dt

