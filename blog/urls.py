from django.contrib import admin
from django.urls import path,include

from . import views

urlpatterns = [
    path('',views.BlogView,name='blogs'),
    path('detail/<int:pk>',views.DetailBlogView,name='blogdetail'),
    path('comment/<int:pk>',views.AddComment,name='addcomment'),
    path('tag/<int:pk>',views.AddTag,name='addtag'),




]