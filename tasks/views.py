# -*- coding: utf-8 -*-
import json, csv
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template.loader import render_to_string
from django.shortcuts import render, render_to_response
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView

from django.contrib.auth.models import User

from .forms import UserForm, UserProfileForm, TaskForm, RewardForm, TaskAddressFileForm
from .models import UserProfile, Task, TaskReward, TaskAddress, TaskAddressFile, AddressResult

#HomeView page - Profile
class HomeView(TemplateView):
	context_object_name = ''   
	template_name = 'tasks/my_profile.html'
	#queryset = Task.objects.all()

	def get_context_data(self, **kwargs):
		context = super(HomeView, self).get_context_data(**kwargs)
		actual_user = self.request.user
		
		context['my_user'] =  User.objects.get(username=actual_user)
		user_profile_qs = context['my_user_profile'] = UserProfile.objects.get(user=actual_user)
		
		created_tasks = context['created_tasks'] = Task.objects.filter(creator=actual_user)
		created_rewards = context['created_rewards'] = TaskReward.objects.filter(task__creator=actual_user)
			
		context['collaborating_tasks'] = Task.objects.filter(my_tasks=user_profile_qs)
		users_w_rewards = context['users_w_rewards'] = UserProfile.objects.filter(my_rewards=created_rewards)
		
		for task in created_tasks:
			collaborating_users = UserProfile.objects.filter(my_tasks=task)
			if collaborating_users.count() > 0:
				for col_user in collaborating_users:
					# print task
					# print col_user
					user_task_answers = AddressResult.objects.filter(user=col_user.user, address__task_name=task).count()
					# print user_task_answers
					task_reward = TaskReward.objects.filter(task=task)
					if task_reward.exists():
						for the_reward in task_reward:
							if user_task_answers >= the_reward.reward_goal:
								if UserProfile.objects.filter(my_rewards=the_reward).exists():
									pass
									print "You have the reward"
								else:
									col_user.my_rewards.add(the_reward)
									col_user.save()
									print "You got the reward (saved)"

							else:
								if UserProfile.objects.filter(my_rewards=the_reward).exists():
									col_user.my_rewards.remove(the_reward)
									col_user.save()
									print "No reward yet (removed)"
								else:
									print "No reward yet"

		actual_rewards = []
		my_users_w_rewards = [] 
		for task in created_tasks: #tareas creadas por mi
			task_reward = TaskReward.objects.filter(task=task) #Ver que TaskRewards hay para mis tareas
			if task_reward.count() > 0: #If task reward exists /Si las hay, al menos una
				for reward in task_reward:
					print reward
					actual_rewards.append(reward)
					collab_users = UserProfile.objects.filter(my_rewards=reward)
					if collab_users.count() > 0:
						for col_user in collab_users:
							print col_user
							my_users_w_rewards.append(col_user)
					else:
						pass
						print "No user gets this reward"
			else:
				pass
				print "Task with no rewards offered"

		 
		context['rewards_offered'] = actual_rewards
		context['my_users_w_reward'] = my_users_w_rewards 

		return context

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(HomeView, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs): 
		context = self.get_context_data(**kwargs)
		return self.render_to_response(context) 

# ----------------------------- #
	
class AjaxTemplateMixin(object):
    
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, 'ajax_template_name'):
            split = self.template_name.split('.html')
            split[-1] = '_inner'
            split.append('.html')
            self.ajax_template_name = ''.join(split)
        if request.is_ajax():
            self.template_name = self.ajax_template_name
        return super(AjaxTemplateMixin, self).dispatch(request, *args, **kwargs)

# ----------------------------- #

#Create views
class TaskCreateView(SuccessMessageMixin, AjaxTemplateMixin, CreateView):
	model = Task
	form_class = TaskForm
	template_name = 'tasks/task_create_form.html'
	
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(TaskCreateView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super(TaskCreateView, self).get_context_data(**kwargs)
	    # Add in a QuerySet of all the books
	    context['title_action'] = 'New Crowd-GeoCoding Task - by'
	    return context

	def form_valid(self, form):
		data = form.save(commit=False)
		user = self.request.user
		data.creator = user
		data.save()
		return super(TaskCreateView, self).form_valid(form)

class RewardCreateView(SuccessMessageMixin, AjaxTemplateMixin, CreateView):
	model = TaskReward
	form_class = RewardForm
	template_name = 'tasks/reward_create_form.html'
	
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(RewardCreateView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super(RewardCreateView, self).get_context_data(**kwargs)
	    # Add in a QuerySet of all the books
	    context['title_action'] = 'New Task Reward- by'
	    return context

	def get_form(self, form_class):
	    form = super(RewardCreateView,self).get_form(form_class) #instantiate using parent
	    #user_tasks_list = TaskReward.task.objects.filter(creator = self.request.user)
	    my_tasks = Task.objects.filter(creator= self.request.user.pk)
	    tasks_with_reward = []
	    for task in my_tasks:
	    	if TaskReward.objects.filter(task=task).count() != 0:
	    		tasks_with_reward.append(task.pk)
	    try:
	    	form.fields['task'].queryset = Task.objects.filter(Q(status="SB") | Q(status="IP"), reward_is_offered=True, creator=self.request.user).exclude(pk__in=tasks_with_reward)
	    	# form.fields['task'].queryset = Task.objects.exclude(name__in=tasks_with_reward.name)
	    	return form
	    except:
	    	pass

# ----------------------------- #

#Detail views
class TaskDetailView(SuccessMessageMixin, AjaxTemplateMixin, DetailView):
	model = Task
	form_class = TaskForm
	template_name = 'tasks/task_view_form.html'
	success_url = reverse_lazy('my-profile')

	def dispatch(self, request, *args, **kwargs):
		self.task_id = kwargs['pk']
		return super(TaskDetailView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super(TaskDetailView, self).get_context_data(**kwargs)
	    # Add in a QuerySet of all the books
	    context['title_action'] = 'Crowd-GeoCoding Task Details'
	    return context

class RewardDetailView(SuccessMessageMixin, AjaxTemplateMixin, DetailView):
	model = TaskReward
	template_name = 'tasks/reward_view_form.html'
	success_url = reverse_lazy('my-profile')

	def dispatch(self, request, *args, **kwargs):
		self.taskreward_id = kwargs['pk']
		return super(RewardDetailView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super(RewardDetailView, self).get_context_data(**kwargs)
	    # Add in a QuerySet of all the books
	    context['title_action'] = 'Reward Details'
	    return context

# ----------------------------- #

#Update Views
class TaskUpdateView(SuccessMessageMixin, AjaxTemplateMixin, UpdateView):
	model = Task
	form_class = TaskForm
	template_name = 'tasks/task_edit_form.html'
	success_url = reverse_lazy('my-profile')
	success_message = "The task was save correctly!"

	def user_passes_test(self, request):
		if request.user.is_authenticated():
			self.object = self.get_object()
			return self.object.creator == request.user
		return False

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		if not self.user_passes_test(request):
			return redirect_to_login('/my-profile/')
		self.task_id = kwargs['pk']
		return super(TaskUpdateView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super(TaskUpdateView, self).get_context_data(**kwargs)
	    # Add in a QuerySet of all the books
	    context['title_action'] = 'Edit Crowd-GeoCoding Task - by'
	    return context

class RewardUpdateView(SuccessMessageMixin, AjaxTemplateMixin, UpdateView):
	model = TaskReward
	form_class = RewardForm
	template_name = 'tasks/reward_edit_form.html'
	success_url = reverse_lazy('my-profile')
	success_message = "The reward was save correctly!"

	def user_passes_test(self, request):
		if request.user.is_authenticated():
			self.object = self.get_object()
			return self.object.task.creator == request.user
		return False

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		if not self.user_passes_test(request):
			return redirect_to_login('/my-profile/')
		self.task_id = kwargs['pk']
		return super(RewardUpdateView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super(RewardUpdateView, self).get_context_data(**kwargs)
	    # Add in a QuerySet of all the books
	    context['title_action'] = 'Edit Task Reward - by'
	    return context

class UserUpdateView(UpdateView):
	model = User
	form_class = UserForm
	template_name = 'form.html'
	success_url = reverse_lazy('my-profile')

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(UserUpdateView, self).dispatch(*args, **kwargs)

	def get_object(self):
	    return self.request.user

class UserProfileUpdateView(UpdateView):
	model = UserProfile
	form_class = UserProfileForm
	template_name = 'form.html'
	success_url = reverse_lazy('my-profile')

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(UserProfileUpdateView, self).dispatch(*args, **kwargs)

	def get_object(self, queryset=None):
		user_profile, created = UserProfile.objects.get_or_create(user=self.request.user)
		return user_profile

# ----------------------------- #

#List Views
class TaskListView(ListView):
	model = Task
	paginate_by='3'
	queryset = Task.objects.filter(status='IP').order_by('-created')


class RewardListView(ListView):
	model = TaskReward
	paginate_by='3'
	queryset = TaskReward.objects.filter(task__reward_is_offered=True, task__status='IP').order_by('task', '-updated')

#List view de rewards filtradas por reward id

# ----------------------------- #

#Delete view
class TaskDeleteView(SuccessMessageMixin, AjaxTemplateMixin, DeleteView):
	model = Task
	success_url = reverse_lazy('my-profile')
	success_message = "Deleted Successfully"
	template_name = 'tasks/task_delete_form.html'

	def user_passes_test(self, request):
		if request.user.is_authenticated():
			self.object = self.get_object()
			return self.object.creator == request.user
		return False

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		if not self.user_passes_test(request):
			return redirect_to_login('/my-profile/')
		task_object = super(TaskDeleteView, self).dispatch(request, *args, **kwargs)
		return task_object

class RewardDeleteView(SuccessMessageMixin, AjaxTemplateMixin, DeleteView):
	model = TaskReward
	success_url = reverse_lazy('my-profile')
	success_message = "Deleted Successfully"
	template_name = 'tasks/reward_delete_form.html'

	def user_passes_test(self, request):
		if request.user.is_authenticated():
			self.object = self.get_object()
			return self.object.task.creator == request.user
		return False

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		if not self.user_passes_test(request):
			return redirect_to_login('/my-profile/')
		reward_object = super(RewardDeleteView, self).dispatch(request, *args, **kwargs)
		return reward_object

# ----------------------------- #

       
class TaskSubscribeView(AjaxTemplateMixin, TemplateView):
	template_name = 'tasks/task_subscribe_message.html'

# ----------------------------- #

#Subir los datos
class AddressFileView(FormView):
	template_name = 'tasks/upload_file_form.html'
	form_class = TaskAddressFileForm

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(AddressFileView, self).dispatch(*args, **kwargs)

	def get_form(self, form_class):
	    form = super(AddressFileView,self).get_form(form_class) #instantiate using parent
	    try:
	    	form.fields['task'].queryset = Task.objects.filter(creator=self.request.user, status='SB')
	    	return form
	    except:
	    	pass

	def form_valid(self, form):
		task_obj = form.cleaned_data['task']
		file = TaskAddressFile(task= task_obj, address_file=self.get_form_kwargs().get('files')['address_file'])
		file.save()
		self.id = file.id
		#proceso los datos
		file_path = file.address_file.path
		with open(file_path,'rU') as csvfile:
			reader = csv.reader(csvfile)
			next(csvfile)
			address_list = [ ]
			for row in reader:
				#print row[0]
				try:
					#address_list.append(row[0])
					address_obj = TaskAddress(task_name=task_obj,address_text= row[0])
					address_obj.save()
					address_list.append(address_obj.address_text)
					#print my_filter_qs
					#Entry.objects.filter(id__in=[1, 3, 4])
					#
					#print my_filter_qs
				except Exception, e:
					#messages.error(self.request, "Some addresses have special characters, please upload your file again using UTF-8 encoding.")
					file.save()
					file.delete()
					TaskAddress.objects.filter(address_text__in=address_list).delete()	
					print address_list

		messages.success(self.request, 'The addresses data file was uploaded correctly')
		return HttpResponseRedirect(self.get_success_url())

	def get_success_url(self):
		return reverse('my-profile')
		#return reverse('file', kwargs={'pk': self.id})

class AddressFileDetailView(DetailView):
	model = TaskAddressFile
	template_name = 'tasks/upload_file_view.html'
	#context_object_name = 'image'

	def user_passes_test(self, request):
		if request.user.is_authenticated():
			self.object = self.get_object()
			return self.object.task.creator == request.user
		return False

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		if not self.user_passes_test(request):
			return redirect_to_login('/my-profile/')
		file_object = super(AddressFileDetailView, self).dispatch(request, *args, **kwargs)
		return file_object

class AddressFileListView(ListView):
	model = TaskAddressFile
	template_name = 'form.html'
	#context_object_name = 'image'
	queryset = TaskAddressFile.objects.all()






#Pruebas
@login_required
def my_profile(request):
	if request.method == "GET":
		user_tasks_list = Task.objects.filter(creator = request.user)
		context = {'user_tasks_list': user_tasks_list}
		template = 'my_profile1.html'
		return render(request, template, context)
		
	context = { }
	template = 'my_profile1.html'
	return render(request, template, context)





# class NewFormView(FormView):
# 	template_name = 'form.html'
# 	form_class = UpdateUserForm
# 	initial_data = {'description':'Take some time to tell the world something about you...'}
# 	success_url = '/my-profile'

# 	def form_valid(self, form):
# 		print self
# 		return super(NewFormView, self).form_valid(form)

# 	def get_initial(self):
# 		return self.initial_data



