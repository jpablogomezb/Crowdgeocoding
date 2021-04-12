from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib import admin
from tasks.views import HomeView, UserUpdateView, UserProfileUpdateView, \
    AddressFileView, AddressFileDetailView, TaskListView, RewardListView, \
    TaskCreateView, TaskUpdateView, TaskDetailView, TaskDeleteView, TaskSubscribeView, \
    RewardCreateView, RewardDetailView, RewardUpdateView, RewardDeleteView
from tasks.ajax import post_task, save_answer, get_address, get_geocoders_results, get_geocoders_output
from map.views import MapTaskView

urlpatterns = patterns('',
	(r'^accounts/', include('allauth.urls')),
    url(r'^choose-language$', 'django.views.i18n.set_language', name='set_language'),
    #App Home
    url(r'^$', 'app.views.home', name='home'),
    #CrowdGeocode Map
    # url(r'^map/$', 'map.views.map', name='map'),
    url(r'^map/task/(?P<pk>\d+)/$', MapTaskView.as_view(), name='map-task'),
    #Home/Profile Site
    url(r'^my-profile/$', HomeView.as_view(), name='my-profile'),
    url(r'^my_profile/$', 'tasks.views.my_profile', name='my_profile'),
    #Edit user profile views
    url(r'^my-profile/user/edit/',  UserUpdateView.as_view(), name='user-edit'),
    url(r'^my-profile/description/edit/',  UserProfileUpdateView.as_view(), name='profile-edit'),

    #List with all tasks
    url(r'^tasks/$', TaskListView.as_view(), name='all_tasks'),
    #Task creation
    url(r'^task-new/$', TaskCreateView.as_view(), name='task-new'),
    #Detail of 1 task
    url(r'^task-detail/(?P<pk>\d+)/$', TaskDetailView.as_view(), name='task-detail'),
    #Task edition
    url(r'^task-edit/(?P<pk>\d+)/$', TaskUpdateView.as_view(), name='task-edit'),
    #Task delete
    url(r'^task-delete/(?P<pk>\d+)/$', TaskDeleteView.as_view(), name='task-delete'),
    #Task subscribe modal confirmation message
    url(r'^task-subscribe/$', TaskSubscribeView.as_view(), name='task-subscribe'),
    #List with all rewards
    url(r'^rewards/$', RewardListView.as_view(), name='all_rewards'),
    #Reward creation
    url(r'^reward-new/$', RewardCreateView.as_view(), name='reward-new'),
    #Detail of 1 reward
    url(r'^reward-detail/(?P<pk>\d+)/$', RewardDetailView.as_view(), name='reward-detail'),
    #Reward edition
    url(r'^reward-edit/(?P<pk>\d+)/$', RewardUpdateView.as_view(), name='reward-edit'),
    #Reward delete
    url(r'^reward-delete/(?P<pk>\d+)/$', RewardDeleteView.as_view(), name='reward-delete'),

    #Other URLs
    url(r'^access_denied/$', TemplateView.as_view(template_name='access_denied.html'), name='access_denied'),
    #Contact
    url(r'^contact/$', 'contact.views.contacto', name='contact'),
    
    #Upload file
    url(r'^upload-file/$', AddressFileView.as_view(), name='upload-file'),
    #View file
    url(r'^file/(?P<pk>\d+)/$', AddressFileDetailView.as_view(),
        name='file'),
    
    #AJAX PROCESSING#
    url(r'^get-address/$', 'tasks.ajax.get_address', name='get-address'),
    url(r'^geocode/$', 'tasks.ajax.get_geocoders_output', name='geocode'),
    #url(r'^get-geocoders/$', 'tasks.ajax.get_geocoders_results', name='get-geocoders'),
    #POST to subscribe to a task
    url(r'^post-task/$', 'tasks.ajax.post_task', name='post-task'),
    #POST to save one task answers
    url(r'^save-answer/$', 'tasks.ajax.save_answer', name='save-answer'),


    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
