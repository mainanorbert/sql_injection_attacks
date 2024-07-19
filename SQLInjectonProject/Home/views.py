from django.shortcuts import render

# Create your views here.

def home(request):
    """
    View function for home page of the app.
    """
    username = request.session.get('username', None)
    db = request.session.get('db', None)
    db_user = request.session.get('db_user', None)
    user_details = request.session.get('user_details', None)
    return render(request, 'home.html', {'username': username, 'db': db, 'db_user': db_user, 'user_details': user_details})

def about_view(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')
