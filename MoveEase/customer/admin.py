from django.contrib import admin

# Register your models here.
from . models import User, CustomerTable

admin.site.register(User)
admin.site.register(CustomerTable)