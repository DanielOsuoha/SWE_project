from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import SignUpForm

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'
    redirect_authenticated_user = True

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'authentication/signup.html'
    success_url = reverse_lazy('core:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('core:index')
        return super().get(*args, **kwargs)
