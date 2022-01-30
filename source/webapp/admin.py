from django.contrib import admin
from webapp.models import Post, PostVote, Comment


class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('vote_amount',)


admin.site.register(Post, PostAdmin)
admin.site.register(PostVote)
admin.site.register(Comment)