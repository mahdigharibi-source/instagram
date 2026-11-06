from django.core.exceptions import ValidationError
from django.db import models
from accounts.models import CustomUser


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        abstract = True


class Profile(Base):
    user = models.OneToOneField(
        to=CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profile',
    )
    username = models.CharField(
        max_length=64,
        unique=True,
    )
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to="profiles/", null=True, blank=True)
    # comments
    # likes

    def __str__(self):
        return f"{self.username}"

class Post(Base):
    user = models.ForeignKey(
        to=Profile,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    caption = models.TextField(max_length=1000, blank=True)
    # likes
    # images
    # comments

    def __str__(self):
        return f"{self.caption[:10]}"

    def clean(self):
        super().clean()
        if self.pk and not self.images.exists():
            raise ValidationError("a post must have an image")

class Images(Base):
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name='images',
    )
    image = models.ImageField(upload_to="images/")


class Comment(Base):
    user = models.ForeignKey(
        to=Profile,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField(max_length=500)

    def __str__(self):
        return f"{self.text[:10]}"


class Likes(Base):
    user = models.ForeignKey(
        to=Profile,
        on_delete=models.CASCADE,
        related_name='likes',
    )
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name='likes',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "post"],
                name="unique_user_post_like"
            )
        ]
