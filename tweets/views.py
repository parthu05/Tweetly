from django.shortcuts import render,redirect
from .forms import customLoginForm, customRegisterForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(req):
    return render(req, 'home.html')

def login_view(request):
    form = customLoginForm(request, data=request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, 'Login successful!')
        return redirect('home')
    elif request.method == 'POST':
        messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html', {'form': form})


def register(req):
    form = customRegisterForm(req.POST or None)
    if req.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(req, user)
            messages.success(req, 'Registration successful!')
            return redirect('home')
        else:
            messages.error(req, 'Unsuccessful registration. Invalid information.')
    return render(req, 'register.html', {'form': form})

def logout_view(req):
    logout(req)
    messages.info(req, 'You have successfully logged out.')
    return redirect('login')

