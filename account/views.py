from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.urls import reverse
from .forms import MyUserCreationForm, UserSignInForm

def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            messages.success(request, f'Welcome to Campus Shoppy, {username}! Your account has been created successfully.')
            # Redirect to next page or home
            next_page = request.GET.get('next', '/')
            return redirect(next_page)
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'account/signup.html', {'form': form})
    else:
        form = MyUserCreationForm()
        return render(request, 'account/signup.html', {'form': form})


def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserSignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                # Redirect to next page or home
                next_page = request.GET.get('next', '/')
                return redirect(next_page)
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
        return render(request, 'account/signin.html', {'form': form})
    else:
        form = UserSignInForm()
        return render(request, 'account/signin.html', {'form': form})


def signout(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')

