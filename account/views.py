from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import  MyUserCreationForm

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
            return redirect('/')
        else:
            return render(request, 'account/signup.html', {'form': form})
    else:
        form =  MyUserCreationForm()
        return render(request, 'account/signup.html', {'form': form})


def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        return render(request, 'account/signin.html', {'form': form})
    else:
        form = AuthenticationForm(request)
        return render(request, 'account/signin.html', {'form': form})


def signout(request):
    logout(request)
    return redirect('home')

