from django.contrib import admin

# Register your models here.
from .models import Contact
from .forms import ContactForm

class ContactAdmin(admin.ModelAdmin):
	form = ContactForm
	#class Meta:
	#	model = Contact

admin.site.register(Contact,ContactAdmin) 
