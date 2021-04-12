# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings

# Create your models here.

class Contact(models.Model): 
	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
	name = models.CharField(max_length=120, default='', blank=True)
	email = models.EmailField()
	subject = models.CharField(max_length=120)
	message = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __unicode__(self):
		if self.name:
			return "%s %s" %(self.name, " sent a message!")
		else:
			return "%s %s" %(self.email, " sent a message!")

