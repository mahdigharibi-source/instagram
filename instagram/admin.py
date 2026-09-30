from django.contrib import admin

from instagram.models import Profile, Post, Images, Comment, Likes

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Images)
admin.site.register(Comment)
admin.site.register(Likes)
