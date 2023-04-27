from django.contrib import admin
from .models import category, sms, sub_category , lang , Complaint

admin.site.register(category)
admin.site.register(sub_category)
admin.site.register(lang)
admin.site.register(Complaint)

class SmsAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_cat_name', 'sub_cat_name','sms' ,'status')

    def get_cat_name(self, obj):
        return obj.sub_cat_name.cat_name
    get_cat_name.short_description = 'Category'

admin.site.register(sms, SmsAdmin)
