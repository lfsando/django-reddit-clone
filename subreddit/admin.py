from django.contrib import admin

from subreddit.models import Subreddit, Post, LinkPost, SelfPost, Comment


@admin.register(Subreddit)
class SubredditAdmin(admin.ModelAdmin):
    pass


class LinkPostInline(admin.TabularInline):
    model = LinkPost


class SelfPostInline(admin.TabularInline):
    model = SelfPost


@admin.register(LinkPost)
class LinkPostAdmin(admin.ModelAdmin):
    pass


@admin.register(SelfPost)
class SelfPostAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = []

    def get_inline_instances(self, request, obj: Post = None):
        inlines = self.inlines
        # Display inline when the object has been saved and a team has been selected.
        if obj:
            if obj.post_type == Post.SELFPOST:
                inlines = [SelfPostInline, ]
            else:
                inlines = [LinkPostInline]
        return [inline(self.model, self.admin_site) for inline in inlines]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass