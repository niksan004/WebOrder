from django.shortcuts import render, redirect
from django.views.generic.edit import FormView, View
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login

from .forms import CustomUserCreationForm, CustomUserLoginForm, CustomUserChangeForm

from .models import User
from graphs.models import EmployeeWorkingHours


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    success_url = ''

    def form_valid(self, form):
        form.save()
        user_log = EmployeeWorkingHours.create(User.objects.get(username=form.cleaned_data.get('username')))
        user_log.save()
        return super(RegisterView, self).form_valid(form)


class Login(LoginView):
    authentication_form = CustomUserLoginForm
    form_class = CustomUserLoginForm
    template_name = 'registration/login.html'
    success_url = ''

    def form_valid(self, form):
        login(self.request, form.get_user())

        return super(LoginView, self).form_valid(form)
