from __future__ import unicode_literals

from django.db import models

class Alarm(models.Model):
	alarm_time = models.DateTimeField()
	ip_address = models.GenericIPAddressField()

	def __unicode__(self):
		return u'time: %s for IP : %s' % (self.alarm_time, self.ip_address)
