from typing import Optional, Union

from django import template

from subreddit.models import Votable, Post, Comment, Vote

register = template.Library()


@register.filter(name="vote_status")
def vote_status(votable: Union[Post, Comment], user=None) -> Optional[str]:
    try:
        if type(votable) is Post:
            user_vote = Vote.objects.get(user=user, post=votable)
        elif type(votable) is Comment:
            user_vote = Vote.objects.get(user=user, comment=votable)
        else:
            return None
        return user_vote.status.lower()
    except Vote.DoesNotExist:
        return None
    except TypeError:
        return None
