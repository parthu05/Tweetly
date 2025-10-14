from django.shortcuts import render,redirect
from .forms import customLoginForm, customRegisterForm, TweetForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(req):
    tweets = req.user.tweet_set.all().order_by('-created_at')
    return render(req, 'home.html', {'tweets': tweets})

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

@login_required
def create_tweet(req):
    if req.method == 'POST':
        form = TweetForm(req.POST, req.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = req.user
            tweet.save()
            messages.success(req, 'Tweet created successfully!')
            return render(req, 'tweetForm.html', { 'form': form })
        else:
            form = TweetForm()
            messages.error(req, 'Error creating tweet. Please check the form.')
    return render(req, 'tweetForm.html',{ 'form': TweetForm() })

