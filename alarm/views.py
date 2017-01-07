import datetime
import unicodedata
import webbrowser
import time
import pytz
import json

from django.shortcuts 			  import render, redirect
from django.core.serializers.json import DjangoJSONEncoder
from alarm.models     			  import Alarm
from django.utils     			  import timezone
from django.utils.timezone 		  import localtime
from views_helper 				  import *

###################################################################################

# Use datetime.datetime AWARE objects for storing time and that only in UTC
# When taking input from the user, always convert it from locatime to UTC and while 
# rendering display it the local timezone. 

###################################################################################
#####################################################################################

def alarm(request):
	"""
	Validate the input given by the user, report the errors and if no errors found  add it to the database.
	"""
	# Create a list for logging all errors in the process
	errors = []

	# Take the current time, date and month
	now = localtime(timezone.now())
	data = {
			'now_str' : now.strftime("%D:%H:%M:%S"),
			'now_month' : now.month,
		   }

	# Create a JSON object for the current and alarm time, so that we can parse it over
	# in HTML 
	js_data = json.dumps(data, cls = DjangoJSONEncoder)
	s_dict = {"now": localtime(timezone.now()), 'errors': errors, 'js_data' : js_data}

	# Check wether the user has set alarm time or duration:
	if "alarm_time" in request.POST and request.POST.get("alarm_time", None) != "":
		# Extract the information about the alarm_time
		alarm_time = uni_to_str(request.POST.get("alarm_time", "Not Set"))
		
		# Make datetime objects.
		try:
			alarm_time = datetime.datetime.strptime(alarm_time, "%d/%m/%Y %H:%M:%S")
		except ValueError:
			errors.append("Please enter valid time.")
			print "Please enter valid time."
			return render(request, "index.html", {'errors' : errors})
		
		alarm_time = convert_to_utc(alarm_time)
		print "alarm_time is %s \n\n\n\n" % alarm_time 	##########
		# Write it to database
		check_and_save(request, alarm_time)
		
		# Preparing HTML variables.
		s_dict = {"alarm_time" : alarm_time, 'now' : now, "errors": []}
		s_dict = check(request, alarm_time, s_dict, errors)

		if not errors:
			return redirect('/success')
	
	elif "alarm_duration" in request.POST:
		# Extract the information about the alarm_time
		duration = uni_to_str(request.POST.get("alarm_duration", "Not Set"))
		print "Duration is %s" % duration
		# Convert from unicode to python string
		try:
			duration = datetime.datetime.strptime(duration, "%d/%m/%Y %H:%M:%S")
			print "Duration after extraction is %s" % duration
		except ValueError:
			errors.append("Please enter valid time. NO STRPTIME ")
			print "Please enter valid time. NO STRPTIME "
			return render(request, "index.html", {'errors' : errors})
		
		# Create time objects
		now = datetime.datetime.now()
		alarm_time = now + datetime.timedelta(hours = duration.hour, minutes = duration.minute, seconds = duration.second)
		print "alarm_time in local time is %s" % alarm_time

		# Convert time from local to UTC timezone
		alarm_time = convert_to_utc(alarm_time)

		print "Now(UTC) is: %s and alarm_time in UTC is %s" % (convert_to_utc(now), alarm_time)
		print "Message is %s" % (request.POST.get("main_message", ""))
		# Save the ip and time in database
		check_and_save(request, alarm_time)	
		
		# Prepare HTML variables.
		s_dict = {"alarm_time" : alarm_time, 'now' : now, "errors" : [], }
		s_dict = check(request, alarm_time, s_dict, errors)

		if not errors:
			return redirect('/success')
	
	# If no request.
	if request.POST.get("alarm_time", None) == "":
		errors.append("Please enter valid Time")

	return render(request, "index.html", s_dict)

def create_alarm(request):
	"""
	The main wrapper around alarm view.
	"""
	ip = get_client_ip(request)
	alarm_time = timezone.now()
	for alarm in Alarm.objects.all():
		if ip == alarm.ip_address:
			alarm_time = alarm.alarm_time
			message = alarm.message
			break

	if not message:
		message = ""
	now = timezone.now()

	# Use localtime for display
	alarm_time_local = localtime(alarm_time)
	data = {
			'now_str' : now.strftime("%D:%H:%M:%S"),
			'alarm_time' : alarm_time.strftime("%D:%H:%M:%S")
		}

	# Create a JSON object for the current and alarm time, so that we can parse it over
	# success.html for comparson.
	
	js_data = json.dumps(data, cls = DjangoJSONEncoder)
	s_dict = {"alarm_time" : alarm_time_local, 'now' : now, 'js_data' : js_data, 'message': message}
	return render(request, "success.html", s_dict)
