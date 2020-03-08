from django.urls import path

from subreddit import views

urlpatterns = [
    path('', views.frontpage, name="frontpage"),
    path('api/vote', views.vote, name="vote")
]