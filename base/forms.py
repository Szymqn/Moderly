from django import forms
from .models import Photo, Slider


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'image']


class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = ['name', 'photos']
