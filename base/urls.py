from django.urls import path
from .views import home, slider, create_slider, add_photo_to_slider, upload_photo, choose_slider

urlpatterns = [
    path('', home, name='home'),
    path('slider/', slider, name='slider'),
    path('upload_photo/', upload_photo, name='upload_photo'),
    path('create_slider/', create_slider, name='create_slider'),
    path('add_photo_to_slider/', add_photo_to_slider, name='add_photo_to_slider'),
    path('choose_slider/', choose_slider, name='choose_slider'),
]
