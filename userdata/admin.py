from django.contrib import admin
from .models import category, sms, sub_category , Complaint, Image , Sticker
from django.utils.html import format_html
# admin.site.register(category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('cat_name', 'display_image')

    def display_image(self, obj):
        if obj.cat_image_link:
            return format_html('<img src="{}" width="50" height="50" />', obj.cat_image_link.url)
        else:
            return '(No image)'

    display_image.short_description = 'Category Image'

admin.site.register(category, CategoryAdmin)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('sub_category', 'image_preview', 'thumbnail_preview')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        else:
            return '(No image)'
    image_preview.short_description = 'Image Preview'

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" width="50" height="50" />', obj.thumbnail.url)
        else:
            return '(No thumbnail)'
    thumbnail_preview.short_description = 'Thumbnail Preview'

admin.site.register(Image, ImageAdmin)
# admin.site.register(lang)
# admin.site.register(Complaint)

class SmsAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_cat_name', 'sub_cat_name','sms' ,'status')

    def get_cat_name(self, obj):
        return obj.sub_cat_name.cat_name
    get_cat_name.short_description = 'Category'

admin.site.register(sms, SmsAdmin)



class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('id','sms','user', 'complaint_text')
admin.site.register(Complaint, ComplaintAdmin)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('sub_cat_name','display_image')

    def display_image(self, obj):
        if obj.Sub_cat_image:
            return format_html('<img src="{}" width="50" height="50" />', obj.Sub_cat_image.url)
        else:
            return '(No image)'

    display_image.short_description = 'Sub Category Image'

admin.site.register(sub_category, SubCategoryAdmin)



class StickerAdmin(admin.ModelAdmin):
    list_display = ('sub_category', 'sticker_preview')

    def sticker_preview(self, obj):
        if obj.sticker:
            return format_html('<img src="{}" width="50" height="50" />', obj.sticker.url)
        else:
            return '(No image)'
    sticker_preview.short_description = 'sticker Preview'

    

admin.site.register(Sticker, StickerAdmin)