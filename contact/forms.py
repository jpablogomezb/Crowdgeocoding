# -*- coding: utf-8 -*-
from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
	    super(ContactForm, self).__init__(*args, **kwargs)
	    #Aquí puedo hacer modificaciones al modelo y la presentación
	    #del formulario
	    #self.fields['name'].required = True
	    #self.fields['name'].widget.attrs['readonly'] = True
	    #self.fields['user'].widget.attrs['disabled'] = True
	    #self.fields['user'].widget = forms.HiddenInput()
	    #self.fields['name'].initial =  'override'
	    
	class Meta:
		model = Contact
		#fields = ('email','name','subject', 'message')
		fields = '__all__'
		#exclude = ['user']
		#widgets = {'user': forms.HiddenInput()} 

