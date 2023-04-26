from django.contrib import admin
from .models import category, sms, sub_category , lang

admin.site.register(category)
admin.site.register(sub_category)
admin.site.register(lang)

class SmsAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_cat_name', 'sub_cat_name','sms')

    def get_cat_name(self, obj):
        return obj.sub_cat_name.cat_name
    get_cat_name.short_description = 'Category'

admin.site.register(sms, SmsAdmin)
