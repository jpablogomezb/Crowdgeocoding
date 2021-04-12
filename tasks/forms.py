# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from .models import UserProfile, Task, TaskReward, TaskAddressFile

class TaskForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
	    super(TaskForm, self).__init__(*args, **kwargs)
	    #Aquí puedo hacer modificaciones al modelo y la presentación
	    #del formulario
	    #self.fields['creator'].widget.attrs['disabled'] = True

	class Meta:
		model = Task
		#fields = '__all__'
		exclude = ['creator']

class RewardForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
	    super(RewardForm, self).__init__(*args, **kwargs)
	    #Aquí puedo hacer modificaciones al modelo y la presentación
	    #del formulario
	    #self.fields['creator'].widget.attrs['disabled'] = True
	    #self.fields['name'].required = True
		#self.fields['name'].widget.attrs['readonly'] = True
		#self.fields['user'].widget.attrs['disabled'] = True
		#self.fields['user'].widget = forms.HiddenInput()
		#self.fields['name'].initial =  'override'

	class Meta:
		model = TaskReward
		fields = '__all__'
		#exclude = ['creator']

class UserForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		#user = kwargs.pop('user','')
		super(UserForm, self).__init__(*args, **kwargs)
	
	class Meta:
	    model = User
	    fields = ['first_name','last_name', 'email']
        
class UserProfileForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		#user = kwargs.pop('user','')
		super(UserProfileForm, self).__init__(*args, **kwargs)
		
	class Meta:
		model = UserProfile
		#fields = ('email','name','subject', 'message')
		fields = ['description', 'my_postal_code']
		#exclude = ['user']

class TaskAddressFileForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(TaskAddressFileForm, self).__init__(*args, **kwargs)
		
	class Meta:
		model = TaskAddressFile
		fields = '__all__'

	






