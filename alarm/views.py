import datetime
import unicodedata
import webbrowser
import time
import pytz

from django.shortcuts import render, redirect
from alarm.models     import Alarm
from django.utils     import timezone
from django.utils.timezone import localtime
from views_helper import *

###################################################################################

# Use datetime.datetime AWARE objects for storing time and that only in UTC
# When taking input from the user, always convert it from locatime to UTC and while 
#  rendering display it the local timezone. 

###################################################################################
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
		#print "Aar Hours : %s Alar inutes: %s" % (alarm_hours, alarm_minutes)
		#print "now in durationm cell is %s" % now
		#print "alarm_time in duration cell is %s" % (alarm_time)
		
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
