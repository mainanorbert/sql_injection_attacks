from django.shortcuts import render

# Create your views here.


def register(request):
    """register page for app"""
    return render(request, 'register.html')


def login(request):
    """login page"""
    return render(request, 'login.html')