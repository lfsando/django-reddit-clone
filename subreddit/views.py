""" Subreddit views
"""
import json
from typing import Optional, Union

from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, get_object_or_404

from subreddit.models import Post, NotAllowedException, Comment, Vote
from user.models import UserProfile


def frontpage(request):
    """ Frontpage of the Internet """
    if request.method == "GET":
        posts = Post.objects.all()
        return render(request, "subreddit/frontpage.html", context={"posts": posts, "user": request.user})


def vote(request):
    """ Vote API"""
    if request.method == "POST":
        data = json.loads(request.body)
        action = data.get("action")
        user: UserProfile = get_object_or_404(UserProfile, pk=request.user.id)
        votable_type = data.get('type')
        votable: Optional[Union[Post, Comment]] = None

        if votable_type == "post":
            votable: Post = get_object_or_404(Post, pk=data.get("entry"))
        elif votable_type == "comment":
            votable: Comment = get_object_or_404(Comment, pk=data.get("entry"))

        if votable:
            try:
                if action == "upvote":
                    votable.upvote_post(user=user)
                elif action == "downvote":
                    votable.downvote_post(user=user)
                elif action == "cancelUpvote" or action == "cancelDownvote":
                    votable.unvote_post(user=user)
            except NotAllowedException:
                return HttpResponseBadRequest()
            user_vote: Optional[Vote] = None
            if votable_type == "post":
                user_vote = Vote.objects.get(user=user, post=votable)
            elif votable_type == "comment":
                user_vote = Vote.objects.get(user=user, comment=votable)
            print(user_vote)

            data = dict(**votable.total_votes(), action=user_vote.status)

            return JsonResponse(data=data, status=200)
