from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404


# Create your views here.
from user.models import UserProfile


def user_profile(request, username):
    user = UserProfile.objects.filter(username__iexact=username)
    if user.exists():
        user = user.first()
        context = {
            "user": user,
            "posts": user.posts
        }
        return render(request, "user/user-profile.html", context=context)
    else:
        raise Http404("página não encontrada")
