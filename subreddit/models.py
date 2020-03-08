from typing import Dict

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from user.models import UserProfile


class NotAllowedException(Exception):
    pass


class Subreddit(models.Model):
    name = models.CharField(max_length=20, unique=True)
    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='Criador')
    creation_date = models.DateTimeField(editable=False, blank=True, null=True, verbose_name="Data de criação")
    modified = models.DateTimeField(blank=True, null=True, verbose_name="Modificado")

    class Meta:
        verbose_name = "Subreddit"
        verbose_name_plural = "Subreddits"

    def save(self, *args, **kwargs):
        """ On save, update timestamps"""
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Subreddit, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Votable(models.Model):
    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="Criador")
    creation_date = models.DateTimeField(editable=False, blank=True, null=True, verbose_name="Data de criação")
    modified = models.DateTimeField(blank=True, null=True, verbose_name="Modificado")

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.modified = timezone.now()
        upvote_post = False
        if not self.id:
            self.creation_date = timezone.now()
            upvote_post = True
        obj = super(Votable, self).save(*args, **kwargs)
        if upvote_post:
            self.upvote_post(self.creator)
        return obj

    def get_vote_object(self, user: UserProfile):
        qs = Vote.objects
        if type(self) is Post:
            qs = qs.get(post=self, user=user)
        elif type(self) is Comment:
            qs = qs.get(comment=self, user=user)
        return qs

    def upvote_post(self, user: UserProfile) -> None:
        try:
            vote = self.get_vote_object(user)
            if vote.status == Vote.UPVOTE:
                # user already upvoted
                raise NotAllowedException("User already upvoted this post")
            else:
                # user already voted and is changing the vote status
                vote.status = Vote.UPVOTE
                vote.save()
        except Vote.DoesNotExist:
            # user first time voting
            if type(self) is Post:
                vote = Vote.objects.create(user=user, post=self, status=Vote.UPVOTE)
            elif type(self) is Comment:
                vote = Vote.objects.create(user=user, comment=self, status=Vote.UPVOTE)

    def downvote_post(self, user: UserProfile):
        try:
            vote = self.get_vote_object(user)
            if vote.status == Vote.DOWNVOTE:
                # user already downvoted
                raise NotAllowedException("User already downvoted this post")
            else:
                # user already voted and is changing the vote status
                vote.status = Vote.DOWNVOTE
                vote.save()
        except Vote.DoesNotExist:
            # user first time voting
            Vote.objects.create(user=user, votable=self, status=Vote.DOWNVOTE)

    def unvote_post(self, user):
        try:
            vote = self.get_vote_object(user)
            vote.status = Vote.UNVOTE
            vote.save()
        except Vote.DoesNotExist:
            # UserPostVote was never created.
            raise NotAllowedException("User never voted on this post")

    def total_votes(self) -> Dict[str, int]:
        qs = Vote.objects
        if type(self) is Post:
            qs = qs.filter(post=self)
        elif type(self) is Comment:
            qs = qs.filter(comment=self)
        upvotes: int = qs.filter(status=Vote.UPVOTE).count()
        downvotes: int = qs.filter(status=Vote.DOWNVOTE).count()
        unvoted: int = qs.filter(status=Vote.UNVOTE).count()
        return dict(upvotes=upvotes, downvotes=downvotes, unvoted=unvoted, total=upvotes - downvotes)


class Post(Votable):
    SELFPOST = "SELF"
    LINKPOST = "LINK"
    POST_TYPE_CHOICES = ((SELFPOST, "Texto"), (LINKPOST, "Link"))

    title = models.CharField(max_length=300, verbose_name="Título")
    subreddit = models.ForeignKey(Subreddit, related_name="posts", on_delete=models.CASCADE)
    post_type = models.CharField(max_length=4, verbose_name="Tipo de Post", choices=POST_TYPE_CHOICES)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    @property
    def content(self):
        if self.post_type == self.LINKPOST:
            return self.link_content
        elif self.post_type == self.SELFPOST:
            return self.self_content

    def __str__(self):
        return f"b/{self.subreddit} • u/{self.creator} • {self.title}"


class Comment(Votable):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", verbose_name="Post")
    text = models.TextField(max_length=10000, verbose_name="Comentário")
    parent = models.ForeignKey('self', related_name="parent_comment", on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return f"u/{self.creator} • {self.post.title} • b/{self.post.subreddit.name}"

    class Meta:
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"


class Vote(models.Model):
    UPVOTE = "UPVOTE"
    DOWNVOTE = "DOWNVOTE"
    UNVOTE = "UNVOTE"
    VOTE_STATUS_CHOICES = ((UPVOTE, "Upvoted"), (DOWNVOTE, "Downvoted"), (UNVOTE, "Unvoted"))

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="Usuário")
    status = models.CharField(max_length=10, choices=VOTE_STATUS_CHOICES, verbose_name="Estado")
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Votos"
        verbose_name_plural = "Votos de Usuário"
        unique_together = ["post", "comment", "user"]

    def save(self, *args, **kwargs):
        if not self.post and not self.comment:
            raise ValidationError("Vote needs to have either self.post or self.comment")
        if self.post and self.comment:
            raise ValidationError("Vote can only have one of self.post or self.comment")
        return super(Vote, self).save(*args, **kwargs)

    def __str__(self):
        return f"u/{self.user.username} • {self.status}"


class PostType(models.Model):
    thumbnail_width = models.IntegerField(default=70, blank=True, null=True)
    thumbnail_height = models.IntegerField(default=50, blank=True, null=True)

    class Meta:
        abstract = True


class LinkPost(PostType):
    url = models.URLField(verbose_name="Link")
    post = models.OneToOneField(Post, verbose_name="Post", on_delete=models.CASCADE, related_name="link_content")
    thumbnail = models.ImageField(upload_to="thumbnail", default="img/link_default.png",
                                  width_field="thumbnail_width", height_field="thumbnail_height")

    class Meta:
        verbose_name = "Link"

    def __str__(self, *args, **kwargs):
        return self.post


class SelfPost(PostType):
    text = models.TextField(max_length=40000, verbose_name="Post")
    post = models.OneToOneField(Post, verbose_name="Post", on_delete=models.CASCADE, related_name="self_content")
    thumbnail = models.ImageField(upload_to="thumbnail", default="img/self_default.png",
                                  width_field="thumbnail_width", height_field="thumbnail_height")

    class Meta:
        verbose_name = "Texto"

    def __str__(self, *args, **kwargs):
        return self.post
