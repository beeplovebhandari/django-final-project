from typing import Any
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages
from django.contrib.auth import login, logout

from apps.commons.utils import validate_email, authenticate_user

from .forms import UserRegistrationForm , UserLoginForm


class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'account/registration.html'
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context ['title'] = "Sign Up"
        return context
    
    def post (self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            messages.success(request, "An Account Activation Email Has Been Sent To You !!")
            response = self.form_valid(form)
            user = self.object
            # send account activation mail(request, user)
            return response
        else:
            return self.form_invalid(form)
        
class UserLoginView(CreateView):
    template_name = "account/login.html"
    success_url = reverse_lazy("home")
    form = UserLoginForm

    def get(self, request, *args, **kwargs):
        return render (request, self.template_name, context={"title" : "login", "form" : self.form})
    
    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        username_or_email = request.POST['username_or_email']
        password = request.POST['password']
        if validate_email(username_or_email):
            user = authenticate_user(password, email= username_or_email)
        else:
             user = authenticate_user(password, username= username_or_email)
        if user is not None:
            login(request, user)
            messages.success(request, "User Logged In Sucessfully !! ")
            return redirect ('home')
        messages.error (request, "Invalid username or password !!")
        return redirect ('user_login')


def user_logout(request):
    logout(request)
    messages.success(request , "User Logged Out !!")
    return redirect("home")
            