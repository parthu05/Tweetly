from typing import Any


from django.shortcuts import render,redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .forms import customLoginForm, customRegisterForm, TweetForm, CommentForm
from .models import Tweet, Like, Comment
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(req):
    tweets = (
        Tweet.objects.select_related('user')
        .prefetch_related('likes', 'comments', 'comments__user')
        .order_by('-created_at')
    )
    liked_tweet_ids = set[Any](
        Like.objects.filter(user=req.user, tweet__in=tweets).values_list('tweet_id', flat=True)
    )
    return render(req, 'home.html', {
        'tweets': tweets,
        'liked_tweet_ids': liked_tweet_ids,
        'comment_form': CommentForm(),
    })

@login_required
def my_tweets(req):
    tweets = Tweet.objects.filter(user=req.user).order_by('-created_at')
    return render(req, 'tweets.html', {'tweets': tweets})

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
            return redirect('home')
        messages.error(req, 'Error creating tweet. Please check the form.')
        return render(req, 'tweetForm.html', { 'form': form })
    return render(req, 'tweetForm.html', { 'form': TweetForm() })


@login_required
@require_POST
def like_toggle(req, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    like, created = Like.objects.get_or_create(tweet=tweet, user=req.user)
    if not created:
        like.delete()
    return redirect('home')


@login_required
@require_POST
def add_comment(req, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    form = CommentForm(req.POST)
    if form.is_valid():
        comment: Comment = form.save(commit=False)
        comment.tweet = tweet
        comment.user = req.user
        comment.save()
        return redirect('home')
    messages.error(req, 'Could not add comment')
    return redirect('home')

