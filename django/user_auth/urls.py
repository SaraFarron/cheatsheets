from django.urls import path
from . import views


app_name = 'user_auth'

urlpatterns = [
    path('login', views.LoginPage.as_view(), name='login'),
    path('logout', views.LogoutUser.as_view(), name='logout'),
    path('register', views.RegisterPage.as_view(), name='register'),
    path('user', views.Profile.as_view(), name='profile'),
]
