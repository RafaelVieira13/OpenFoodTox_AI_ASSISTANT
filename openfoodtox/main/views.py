from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(response):
    return render(response, "main/index.html", {})

def specific(response):
    return HttpResponse("list1")

def getResponse(response):
    userMessage = response.GET.get('userMessage')
    return HttpResponse(userMessage)

