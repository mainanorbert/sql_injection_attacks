from django.urls import path
from . import views
# from Home import views as home_views 



urlpatterns = [
     path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    # path('', home_views.home, name='home'),
   
]
