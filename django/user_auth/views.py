from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from .decorators import unauthenticated_user


class LoginPage(View):

    @method_decorator(unauthenticated_user)
    def get(self, request):

        form = AuthenticationForm()
        return render(request, 'user_auth/login.html', {'form': form})

    @method_decorator(unauthenticated_user)
    def post(self, request):

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('user_auth:profile')

        else:
            messages.info(request, 'Username or password is incorrect')

        context = {}
        return render(request, 'user_auth/login.html', context)


class RegisterPage(View):

    @method_decorator(unauthenticated_user)
    def get(self, request):

        form = UserCreationForm()
        return render(request, 'user_auth/register.html', {'form': form})

    @method_decorator(unauthenticated_user)
    def post(self, request):

        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('user_auth:profile')

        return render(request, 'user_auth/register.html', {'form': form})


class LogoutUser(View):

    def get(self, request):

        logout(request)
        return redirect('user_auth:login')


class Profile(View):

    @method_decorator(login_required(login_url='user_auth:login'))
    def get(self, request):

        user = User.objects.get(username=request.user)

        context = {'user': user}
        return render(request, 'user_auth/profile.html', context)
