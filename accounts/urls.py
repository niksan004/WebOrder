from django.urls import path
from django.contrib.auth.views import LoginView

from . import views

urlpatterns = [
    path('signup', views.SignUpView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
    # path('logout', views.LogoutView.as_view(), name='logout'),
]