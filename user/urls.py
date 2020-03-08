from django.urls import path

from user import views

urlpatterns = [
    path(route='<str:username>', view=views.user_profile, name="user_profile"),
]
