# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from allauth.account.signals import user_signed_up, user_logged_in
from django.db import models
from django.dispatch import receiver
from django.contrib.gis.db import models as gismodels 


# Create your models here.
from django.contrib.auth.models import User

class Task(models.Model):
	#id = Django creates an automatic id as a primary key data field
	creator = models.ForeignKey(User, related_name='creator')
	name = models.CharField(max_length=60, null=False, blank=False)
	description = models.TextField(null=False, blank=False)
	max_number_answers = models.SmallIntegerField(null=False, blank=False, help_text="Please enter the number of task answers needed for an address to be considered completed.")
	null_number_answers = models.SmallIntegerField(null=False, blank=False, help_text="Please enter the number of null task answers to consider an address invalid.")
	reward_is_offered = models.BooleanField(default=False)
	STANDBY = 'SB'
	IN_PROCESS = 'IP'
	COMPLETED = 'F'
	STATUS_CHOICES = (
	    (STANDBY, 'Standby'),
	    (IN_PROCESS, 'In process'),
	    (COMPLETED, 'Completed'),
	)
	status = models.CharField(max_length=2,
                                      choices=STATUS_CHOICES,
                                      default=STANDBY)
    #status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=IN_PROCESS)
	created = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return "%s %s" %("Task name: ", self.name)

	def get_absolute_url(self):
		 return reverse('task-detail', kwargs={'pk': self.pk})
       
# ---------------- #
	
class TaskReward(models.Model):
	#id = Django creates an automatic id as a primary key data field
	task = models.ForeignKey(Task)
	name = models.CharField(max_length=25, null=False, blank=False)
	description = models.TextField(null=False, blank=False)
	reward_goal = models.SmallIntegerField(null=False, blank=False, default=100, help_text="Please enter the number of task addresses to be done by a user to obtain the reward.")
	created = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return "%s %s" %("Reward name: ", self.name)

	def get_absolute_url(self):
		 #return '/task/%s/reward/%s/' % (str(self.task_id), self.pk)
		 return reverse('reward-detail', kwargs={'pk': self.pk})

# ---------------- #

class TaskAddress(models.Model):
	#id = Django creates an automatic id as a primary key data field
	task_name = models.ForeignKey(Task)
	address_text = models.CharField(max_length=200, default='', null=False, blank=False)
	IN_PROCESS = 'IP'
	COMPLETED = 'F'
	STAT_CHOICES = (
        (IN_PROCESS, 'In process'),
        (COMPLETED, 'Completed'),
  	)						
	status = models.CharField(max_length=2,
                                  choices=STAT_CHOICES,
                                  default=IN_PROCESS)

	def __unicode__(self):
		return u"%s %s %s" %(self.address_text, " - ", self.task_name)


def upload_to(instance, filename):
		return 'file/%s/task/%s/%s' % (instance.task.creator.username, instance.task.id, filename)

class TaskAddressFile(models.Model):
	task = models.ForeignKey(Task, help_text='Make sure to select one task!')
	address_file = models.FileField(upload_to=upload_to, help_text="Upload a CSV file (UTF-8 encoded) with addresses text data at first column starting at second row. First row is considered as the field title header and is going to be ignored")
	
	def __unicode__(self):
		return unicode(self.address_file)

# ---------------- #

class AddressResult(gismodels.Model):
	#id = Django creates an automatic id as a primary key data field
	user = models.ForeignKey(User)
	address = models.ForeignKey(TaskAddress)
	#final result geometry
	geom_result = gismodels.PointField(null=True)
	objects = gismodels.GeoManager()
	selected_geocoder = models.SmallIntegerField(null=False, default=0)
	coord_Google = models.CharField(max_length=100, null=True)
	coord_Bing = models.CharField(max_length=100, null=True)
	coord_Mapquest = models.CharField(max_length=100, null=True)
	coord_OSM = models.CharField(max_length=100, null=True)
	quality_Google = models.CharField(max_length=100, null=True)
	quality_Bing = models.CharField(max_length=100, null=True)
	quality_Mapquest = models.CharField(max_length=100, null=True)
	quality_OSM = models.CharField(max_length=100, null=True)
	accuracy_Google = models.CharField(max_length=100, null=True)
	accuracy_Bing = models.CharField(max_length=100, null=True)
	accuracy_Mapquest = models.CharField(max_length=100, null=True)
	accuracy_OSM = models.CharField(max_length=100, null=True)
	confidence_Google = models.CharField(max_length=100, null=True)
	confidence_Bing = models.CharField(max_length=100, null=True)
	confidence_Mapquest = models.CharField(max_length=100, null=True)
	confidence_OSM = models.CharField(max_length=100, null=True)
	suggested_Coord = models.CharField(max_length=100, null=True)
	created = models.DateTimeField(auto_now_add=True, auto_now=False)

	class Meta:
		unique_together = ('user', 'address')

	def __unicode__(self):
		return u"%s %s %s" %(self.address, " -by ", self.user)

	# def __str__(self):
	# 	return self.address
			
# ---------------- #

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	description = models.TextField(default='Update this to know more about you!', null=True)
	my_tasks = models.ManyToManyField(Task, related_name='my_tasks', blank=True, help_text="Tasks where I am participating.")
	my_rewards = models.ManyToManyField(TaskReward, related_name='my_rewards', blank=True)
	my_postal_code = models.CharField(max_length=120, null=True, blank=False)
	#ip_address = models.CharField(max_length=120, default ='abc')
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return unicode(self.user)


@receiver(user_signed_up)
def new_user_signed_up(request, user, sociallogin=None, **kwargs):
	profile, created = UserProfile.objects.get_or_create(user_id=user.id)
	profile.save()






