from django.shortcuts import render, redirect
from django.db import connection, IntegrityError
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User

def register(request):
    """Register page for the app"""
    if request.method == 'POST':
        level = request.POST.get('level')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect(f'{request.path}?error=1')
        
        

        if level == 'low':
            query = f"INSERT INTO account_user (username, email, password) VALUES ('{username}', '{email}', '{password}');"
        elif level == 'high':
            query = "INSERT INTO account_user (username, email, password) VALUES (%s, %s, %s);"
        else:
            if level == 'high':
                try:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    messages.success(request, f"User {username} registered successfully!")
                    return redirect('login')
                except IntegrityError:
                    messages.error(request, "Username or email already exists!")
                    return redirect('register')
                except Exception as e:
                    messages.error(request, f"An error occurred: {str(e)}")
                    return redirect('register')

        try:
            with connection.cursor() as cursor:
                if level == 'low':
                    cursor.execute(query)
                else:
                    cursor.execute(query, [username, email, password])
            # messages.success(request, f"User {username} registered successfully!")
            return redirect('login')
        except IntegrityError:
            messages.error(request, "Username or email already exists!")
            return redirect(f'{request.path}?error=1')
            # return redirect('register')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect(f'{request.path}?error=1')
            # return redirect('register')
    
    return render(request, 'register.html')

def login(request):
    """Login page for the app"""
    if request.method == 'POST':
        level = request.POST.get('level')
            
        
        if level == 'low':
            username = request.POST.get('username')
            password = request.POST.get('password')  
            query = f"SELECT * FROM account_user WHERE username = '{username}' AND password = '{password}';"
        elif level == 'high':
            username = request.POST.get('username')
            password = request.POST.get('password')
            query = "SELECT * FROM account_user WHERE username = %s AND password = %s;"
              
        else:
            # query = "SELECT * FROM account_user WHERE username = %s AND password = %s;"            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password!")
                return redirect('login')

        try:
            with connection.cursor() as cursor:
                if level == 'low':
                    cursor.execute(query)
                else:
                    cursor.execute(query, [username, password])
                if len(username) >= 8:
                    user = cursor.fetchall()
                else:
                    user = cursor.fetchone()
        
            if user:
               
                request.session['username'] = username
                request.session['db'] = user[0]
                request.session['db_user'] = user[1]
                if len(username) >= 10:
                    
                    user_details = []                    
                    for usr in user:
                        
                        user_details.append({
                                    'username': usr[0],
                                    'email': usr[1],
                                    'password': usr[2]
                                })
                    request.session['user_details'] = user_details
                messages.success(request, "Successfully Logged in!")
                return redirect('home')  # Redirect to the home page or another page
            else:
                messages.error(request, "Invalid username or password!")
                return redirect(f'{request.path}?error=1')
                
                # return redirect('login')
                # render(request, 'login.html', {'username': username, 'level': level})
                
            
                # return render(request, 'login.html', {'username': username, 'level': level})
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('login')
    
    return render(request, 'login.html')

def logout(request):
    """Logout the user and clear the session"""
    request.session.flush()
    messages.success(request, "You have been logged out successfully!")
    return redirect('home')
