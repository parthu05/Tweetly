from django.shortcuts import render,redirect

# Create your views here.
def home(req):
    return render(req, 'home.html')

def login_view(req):
    return render(req, 'login.html')

def register(req):
    return render(req, 'register.html')
