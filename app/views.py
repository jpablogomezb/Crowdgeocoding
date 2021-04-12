# -*- encoding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, render_to_response
from django.http import HttpResponse


# Create your views here.

def home(request):

	context = { }
	template = 'home.html'
	return render(request, template, context)

