from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path('register/', views.registration, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]