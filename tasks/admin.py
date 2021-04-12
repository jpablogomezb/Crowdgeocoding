from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Task, TaskReward, TaskAddress, AddressResult, UserProfile, TaskAddressFile

admin.site.register(AddressResult,LeafletGeoAdmin)
admin.site.register(TaskAddress)
admin.site.register(TaskReward)
admin.site.register(Task)
admin.site.register(TaskAddressFile)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    
# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)