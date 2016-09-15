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

#####################################################################################

def alarm(request):
	"""
	Validate the input given by the user, report the errors and if no errors found  add it to the database.
	"""
	errors = []
	"""
	if "alarm_time" in request.POST and request.POST.get("alarm_time", None) != "":
		# Extract the information about the alarm_time
		alarm_time_u = request.POST.get("alarm_time", "Not Set")
		
		# Convert from unicode to python string
		alarm_time = uni_to_str(alarm_time_u)
		print "alarm_time is %s" % (alarm_time)

		# Make datetime objects.
		try:
			alarm_time = datetime.datetime.strptime(alarm_time, "%H:%M").time()
		except ValueError:
			errors.append("Please enter valid time.")
			return render(request, "index.html", {'errors' : errors})
		
<<<<<<< HEAD
		now = localtime(timezone.now())
		date_today = now.date()
=======
		now = timezone.now()

		date_today = timezone.now().date()
>>>>>>> master
		alarm_time = timezone.datetime.combine(date_today, alarm_time)
		alarm_time = convert_to_utc(alarm_time)
		
		print "alarm_time_finally is %s" % (alarm_time)
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
	"""
	
	# STEPS:
	# 1. GET INPUT FROM THE USER
	# 2. IF SPECIFIED IN ANY OTHER FORMAT, THEN CONVERT IT TO DATETIME FORMAT - AWARE
	# 3. VALIDATE THE INPUT
	# 4. IF ANY ERRORS FOUND, TE\HEN REPORT IT TO THE USER
	# 5. WRITE IT TO THE DATABASE
	
	time_form = TimeForm()
	duration_form = DurationForm()
	errors = []
	now = timezone.now()	
	s_dict = {'time_form': time_form, 'duration_form': duration_form, 'now': now, 'errors' : errors}
	if request.method == 'POST':
		# Check wether the user has given alarm_time or alarm_duration.
		if "alarm_time" in request.POST and request.POST.get('alarm_time')!= None:
			# Create the time_form instance.
			time_form = TimeForm(request.POST)
			s_dict['time_form'] = time_form
			print "Form1 is %s" % time_form
			# Validate the user input
			if time_form.is_valid():
				# Extract input from user given data.
				cd = time_form.cleaned_data
				alarm_time = cd['alarm_time']
				# Convert the alarm_time into aware datetime object.
				date_today = timezone.now().date()
				alarm_time = timezone.datetime.combine(date_today, alarm_time)
				alarm_time = convert_to_utc(alarm_time)
				print "cleaned data is %s and alarm after conversion: %s" % (cd, alarm_time)
				# Check wether the user has entered the correct time.
				if check(alarm_time):
					# Write it to the database.
					check_and_save(request, alarm_time)
					return redirect('/success')
				# If future time entered, display the error message.
				else:
					s_dict['errors'].append("Please enter Future time.")
					return render(request, "index.html", s_dict) 
			# Report if user has entered invalid input.
			else:
				return render(request, "index.html", s_dict)

		# Check if the user has entered data in the duration form
		if "alarm_duration" in request.POST:
			duration_form = DurationForm(request.POST)
			s_dict['duration_form'] = duration_form 
			print "Errors in duration for: %s" % (duration_form.errors)
			if duration_form.is_valid():
				cd = duration_form.cleaned_data
				print cd
				alarm_duration = cd['alarm_duration']
				now = timezone.now()
				#(alarm_hours, alarm_minutes) = get_alarm_time_from_duration(duration)
				alarm_time = now + datetime.timedelta(hours = alarm_duration.hour, minutes = alarm_duration.minute)
				print "alarm_duration is %s" % alarm_duration
				# Check if the user has entered a future time.
				if check(alarm_time):
					# Write it to the database.
					check_and_save(request, alarm_time)
					return redirect('/success')
				# If future time entered, display the error message.
				else:
					s_dict['errors'].append("Please enter Future time.")
					return render(request, "index.html", s_dict)
			# Report if user has entered invalid input.
			else:
				print duration_form
				print duration_form.errors
				return render(request, "index.html", s_dict)
	else:
		return render(request, 'index.html', s_dict)

	
def create_alarm(request):
	"""
	The main wrapper around alarm view.
	"""
	ip = get_client_ip(request)
	alarm_time = timezone.now()
	for alarm in Alarm.objects.all():
		if ip == alarm.ip_address:
			alarm_time = alarm.alarm_time
			break

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
	s_dict = {"alarm_time" : alarm_time_local, 'now' : now, 'js_data' : js_data}
	return render(request, "success.html", s_dict)
	
