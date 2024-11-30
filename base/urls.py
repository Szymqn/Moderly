from django.urls import path
from django.views.generic.base import TemplateView
from .views import slider, create_slider, add_photo_to_slider, upload_photo

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('slider/', slider, name='slider'),
    path('upload_photo/', upload_photo, name='upload_photo'),
    path('create_slider/', create_slider, name='create_slider'),
    path('add_photo_to_slider/', add_photo_to_slider, name='add_photo_to_slider'),
]
