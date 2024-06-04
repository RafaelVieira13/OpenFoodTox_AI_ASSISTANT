from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(response):
    return render(response, "main/base.html", {})

def home(response):
    return render(response, "main/home.html", {})

def v2(response):
    return HttpResponse('<h1>v2</h1>')