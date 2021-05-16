from django.urls import path

from . import views

urlpatterns = [
    path('about_dishes', views.AboutDishes.as_view(), name='about_dishes'),
    path('about_employees', views.AboutEmployees.as_view(), name='about_employees'),
]