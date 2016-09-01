import datetime
import unicodedata
import webbrowser
import time
import pytz

from django.shortcuts import render, redirect
from alarm.models     import Alarm
from django.utils     import timezone
from django.utils.timezone import localtime

###################################################################################
"""
Use datetime.datetime objects for storing time
"""
###################################################################################
def check_alarm_time(alarm_time):
	"""
	Checks if the alarm_time is in future.
	"""
	# Consider alarm_time is a datetime object.
	now = timezone.now()
	if not alarm_time >= now:
		return False
	return True

def check(request, alarm_time, s_dict, errors):
	"""
	A wrapper around check_alarm_time.
	"""
	if not check_alarm_time(alarm_time):
		error = "Please Enter a future time"
		errors.append(error)
		s_dict["errors"] = error
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
	for alarm in Alarm.objects.all():
		if ip == alarm.ip_address:
			current_alarm = alarm
			break

	if current_alarm == None:
		current_alarm = Alarm(alarm_time=alarm_time, ip_address=ip)
	else:
		current_alarm.alarm_time = alarm_time

	current_alarm.save()

def convert_to_utc(alarm_time):
	"""
	Takes naive alarm_time in local timezone format and converts to UTC aware alarm_time.
	"""
	local = timezone.get_current_timezone()
	local_dt = local.localize(alarm_time, is_dst=None)
	utc_dt = local_dt.astimezone(pytz.utc)
	return utc_dt

#####################################################################################

def alarm(request):
	"""
	Validate the input given by the user, report the errors and if no errors found  add it to the database.
	"""
	errors = []
	if "alarm_time" in request.POST and request.POST.get("alarm_time", None) != "":
		# Extract the information about the alarm_time
		alarm_time_u = request.POST.get("alarm_time", "Not Set")
		
		# Convert from unicode to python string
		alarm_time = uni_to_str(alarm_time_u)
		print alarm_time

		# Make datetime objects.
		try:
			alarm_time = datetime.datetime.strptime(alarm_time, "%H:%M").time()
		except ValueError:
			errors.append("Please enter valid time.")
			return render(request, "index.html", {'errors' : errors})
		
		now = timezone.now()
		date_today = timezone.now().date()
		alarm_time = timezone.datetime.combine(date_today, alarm_time)
		alarm_time = convert_to_utc(alarm_time)
		
		# Write it to database
		check_and_save(request, alarm_time)
		
		# Preparing HTML variables.
		s_dict = {"alarm_time" : alarm_time, 'now' : now}
		s_dict = check(request, alarm_time, s_dict, errors)
		
		if not errors:
			return redirect('/success')
	
	elif "alarm_duration" in request.POST:
		# Extract the information about the alarm_time
		duration_u = request.POST.get("alarm_duration", "Not Set")
		
		# Convert from unicode to python string
		duration = uni_to_str(duration_u)
		(alarm_hours, alarm_minutes) = get_alarm_time_from_duration(duration)
		
		# Create time objects
		now = timezone.now()
		alarm_time = now + datetime.timedelta(hours = alarm_hours, minutes = alarm_minutes)
		print "now in durationm cell is %s" % now
		print "alarm_time in duration cell is %s" % (alarm_time)
		
		# Save the ip and time in database
		check_and_save(request, alarm_time)	
		
		# Prepare HTML variables.
		s_dict = {"alarm_time" : alarm_time, 'now' : now}
		s_dict = check(request, alarm_time, s_dict, errors)
		
		if not errors:
			return redirect('/success')
	
	# If no request.
	if request.POST.get("alarm_time", None) == "":
		errors.append("Please enter valid Time")
	return render(request, "index.html", {"now": localtime(timezone.now()), 'errors': errors,})

def create_alarm(request):
	ip = get_client_ip(request)
	alarm_time = timezone.now()
	for alarm in Alarm.objects.all():
		if ip == alarm.ip_address:
			alarm_time = alarm.alarm_time
			break

	now = timezone.now()

	# Use localtime for display
	alarm_time_local = localtime(alarm_time)
	s_dict = {"alarm_time" : alarm_time_local, 'now' : now}
	return render(request, "success.html", s_dict)
