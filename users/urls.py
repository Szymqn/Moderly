from django.urls import path, include
from .views import login_page, register_page, logout_page

# Define URL patterns
urlpatterns = [
    path('login/', login_page, name='login_page'),
    path('register/', register_page, name='register'),
    path('logout/', logout_page, name='logout'),
    path('auth/', include('allauth.urls')),
]
