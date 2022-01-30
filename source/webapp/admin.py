from django.contrib import admin
from webapp.models import Post, PostVote


class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('vote_amount',)


admin.site.register(Post, PostAdmin)
admin.site.register(PostVote)