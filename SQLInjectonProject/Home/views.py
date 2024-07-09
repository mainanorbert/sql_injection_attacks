from django.shortcuts import render

# Create your views here.

def home(request):
    """
    View function for home page of the app.
    """
    username = request.session.get('username', None)
    return render(request, 'home.html', {'username': username})


