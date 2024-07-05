from django.shortcuts import render, redirect
from django.db import connection, IntegrityError
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login

def register(request):
    """Register page for the app"""
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')
        
        query = f"INSERT INTO account_user (firstname, lastname, username, email, password) VALUES ('{firstname}', '{lastname}', '{username}', '{email}', '{password}');"
        
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
            messages.success(request, f"User {username} registered successfully!")
            return redirect('login')
        except IntegrityError:
            messages.error(request, "Username or email already exists!")
            return redirect('register')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('register')
    
    return render(request, 'register.html')


def login(request):
    """Login page for the app"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        query = f"SELECT * FROM account_user WHERE username = '{username}' AND password = '{password}';"
        
        with connection.cursor() as cursor:
            cursor.execute(query)
            user = cursor.fetchone()
        
        if user:
            messages.success(request, f"Welcome back, {username}!")
            return redirect('home')  # Redirect to the home page or another page
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('login')
    
    return render(request, 'login.html')