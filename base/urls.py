from django.urls import path
from django.views.generic.base import TemplateView
from .views import home, add_photo, photo_list, slider

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('add_photo/', add_photo, name='add_photo'),
    path('photo_list/', photo_list, name='photo_list'),
    path('slider/', slider, name='slider'),
]
