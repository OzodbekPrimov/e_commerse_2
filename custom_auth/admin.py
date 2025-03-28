from django.contrib import admin

# Register your models here.
from custom_auth.models import CustomUser

admin.site.register(CustomUser)