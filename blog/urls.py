from django.contrib import admin
from django.urls import path
import blog.views

urlpatterns = [
    path('', blog.views.home, name="home"),
    path('post/<int:post_id>', blog.views.detail, name = "detail"),
    path('post/new', blog.views.new, name="new"),
]