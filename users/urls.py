from django.urls import path
from .views import *

# Define URL patterns
urlpatterns = [
    path('login/', login_page, name='login_page'),
    path('register/', register_page, name='register'),
    path('logout/', logout_page, name='logout'),
]
