from django import forms
from .models import Image, Sticker

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['sub_category', 'image', 'thumbnail']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': True}),
            'thumbnail': forms.ClearableFileInput(attrs={'multiple': True}),
        }

class StickerUploadForm(forms.ModelForm):
    class Meta:
        model = Sticker
        fields = ['sub_category', 'sticker']
        widgets = {
            'sticker': forms.ClearableFileInput(attrs={'multiple': True}),
        }