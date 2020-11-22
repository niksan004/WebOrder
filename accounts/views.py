from django.shortcuts import render, redirect
from django.views.generic import View, CreateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout

from .forms import SignUpForm


class SignUpView(CreateView):
    success_url = reverse_lazy('login')
    form_class = SignUpForm
    template_name = 'accounts/register.html'
