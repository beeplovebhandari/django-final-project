from django.shortcuts import render
from django.views.generic import ListView
from apps.core.models import Job, JobApplication, Category

class HomeView(ListView):
    template_name = "core/home.html"
    queryset = Job.objects.all()
