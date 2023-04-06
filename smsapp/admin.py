from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import category, sms,sub_category

admin.site.register(category)
admin.site.register(sub_category)
admin.site.register(sms)