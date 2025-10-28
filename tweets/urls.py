from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('create_tweet/', views.create_tweet, name='create_tweet'),
    path('my_tweets/', views.my_tweets, name='my_tweets'),
]