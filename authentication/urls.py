from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUpView , name="signup"),
    path('login/', views.LogInView , name="login"),
    path('logout/', views.LogOutView , name="logout"),



]