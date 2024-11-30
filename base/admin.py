from django.contrib import admin
from .models import Photo, Slider, SliderPhoto, Color, Theme, UserProfile

# Register your models here.
admin.site.register(Photo)
admin.site.register(Slider)
admin.site.register(SliderPhoto)
admin.site.register(Color)
admin.site.register(Theme)
admin.site.register(UserProfile)
