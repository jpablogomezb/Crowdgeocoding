# -*- encoding: utf-8 -*-
import geocoder
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.views.generic import TemplateView, DetailView
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from tasks.models import UserProfile, Task, TaskAddress
#Project Vars
google_api_key = settings.GOOGLE_API
bing_api_key = settings.BING_API
mapbox_api_key = settings.MAPBOX_API

class MapTaskView(DetailView):
	model = Task
	template_name = 'app.html'

	def user_passes_test(self, request):
		if request.user.is_authenticated():
			self.object = self.get_object()
			return UserProfile.objects.filter(user=request.user, my_tasks=self.object).count() == 1
		return False

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		if not self.user_passes_test(request):
			return redirect_to_login('/my-profile/')
		self.task_id = kwargs['pk']
		return super(MapTaskView, self).dispatch(request, *args, **kwargs)
	
	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super(MapTaskView, self).get_context_data(**kwargs)
	    # Add in a QuerySet of all the books
	    context['task_id'] = self.task_id
	    context['google_api'] = google_api_key
	    context['bing_api'] = bing_api_key
	    context['mapbox_api'] = mapbox_api_key
	    return context

@login_required
def map(request):

	context = { }

	return render(request, 'app.html', context)
