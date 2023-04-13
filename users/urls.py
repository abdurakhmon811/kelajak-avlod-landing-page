from django.urls import path
from . import views
from .assistants import generate_token


app_name = 'users'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('get-phone-number-jnsdfc242cc4342c323ch2h3ch234c23/', views.get_phone_numbers, name='get-phone-numbers'),
]