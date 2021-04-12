# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _

from django import forms
from .forms import ContactForm
# Create your views here.

def contacto(request):
	title = _('Need some help?')
	form = ContactForm(request.POST or None)
	form.fields['user'].widget.attrs['disabled'] = True
	confirm_message = None
	if request.user.is_anonymous():
		form.fields['user'].widget = forms.HiddenInput()

	if form.is_valid():
		#store in a model
		new_message = form.save(commit=False)
		#Puedo hacer cambios aquí antes de guardar
		if request.user.is_authenticated():
			user = request.user
			new_message.user = user
			new_message.save()
		else:
			user = None
			new_message.user = user
			new_message.save()
			
		title = _('Thanks')
		confirm_message = _('We have received your message, we will contact you soon!')
		form  = None

	context = {
		'title' : title,
		'form' : form,
		'confirm_message': confirm_message
			}

	template = 'contact.html'
	return render(request, template, context)


