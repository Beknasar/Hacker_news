from django.contrib import admin
from webapp.models import Post


class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('vote_amount',)


admin.site.register(Post, PostAdmin)
