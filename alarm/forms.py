from django import forms

class TimeForm(forms.Form):
	alarm_time = forms.TimeField(required = False)
	
class DurationForm(forms.Form):
	alarm_duration = forms.TimeField()