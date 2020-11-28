from django.shortcuts import render, redirect
from django.views.generic.edit import FormView, View
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login

from .forms import CustomUserCreationForm, CustomUserLoginForm, CustomUserChangeForm


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    success_url = '/orders/cooks'

    def form_valid(self, form):
        form.save()
        return super(RegisterView, self).form_valid(form)


class Login(LoginView):
    authentication_form = CustomUserLoginForm
    form_class = CustomUserLoginForm
    template_name = 'registration/register.html'

    def form_valid(self, form):
        login(self.request, form.get_user())

        return super(LoginView, self).form_valid(form)
