from django import forms
from .models import Photo, Slider, SliderPhoto


class UploadPhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'image', 'description']


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'image']


class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = ['name', 'photos']


class CreateSliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = ['name']


class AddPhotoToSliderForm(forms.Form):
    photo = forms.ModelChoiceField(queryset=Photo.objects.all())
    slider = forms.ModelChoiceField(queryset=Slider.objects.all())
    order = forms.IntegerField(min_value=0, initial=0)


class ChooseSliderForm(forms.Form):
    slider = forms.ModelChoiceField(queryset=Slider.objects.all(), label="Choose Slider")
