from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.html import format_html
from django.db.models import Count
from accounts.models import CustomUser
from .models import Post, Images, Comment, Profile, Likes


# ---------------------------------------------------------------------------
# Inlines
# ---------------------------------------------------------------------------
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "is_active")
    search_fields = ("username", "email")
    list_filter = ("is_active",)

class ImageInline(admin.TabularInline):
    model = Images
    extra = 1
    fields = ("image", "preview", "is_active")
    readonly_fields = ("preview",)

    @admin.display(description="Preview")
    def preview(self, obj):
        if obj.image.url:
            return format_html(
                '<img src="{}" style="max-height:80px;border-radius:6px;" />',
                obj.image.url,
            )
        return "—"


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ("user", "text", "is_active", "created_at")
    readonly_fields = ("created_at",)
    autocomplete_fields = ("user",)
    show_change_link = True


class PostInline(admin.TabularInline):
    """Posts shown on the UserProfile page."""

    model = Post
    extra = 0
    fields = ("caption", "is_active", "created_at")
    readonly_fields = ("created_at",)
    show_change_link = True


# ---------------------------------------------------------------------------
# UserProfile
# ---------------------------------------------------------------------------


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "user",
        "email_display",
        "posts_count",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active", "created_at")
    search_fields = (
        "username",
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
        "bio",
    )
    autocomplete_fields = ("user",)
    readonly_fields = ("created_at", "updated_at", "avatar_preview")
    ordering = ("-created_at",)
    list_per_page = 25
    list_select_related = ("user",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "username",
                    "bio",
                    "profile_picture",
                    # "avatar_preview",
                ),
            },
        ),
        (
            "Status",
            {
                "fields": ("is_active", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    inlines = [PostInline]

    @admin.display(description="Email", ordering="user__email")
    def email_display(self, obj):
        return obj.user.email

    @admin.display(description="Posts", ordering="posts_count")
    def posts_count(self, obj):
        return getattr(obj, "posts_count", obj.posts.count())

    @admin.display(description="Avatar")
    def avatar_preview(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" style="max-height:120px;border-radius:8px;" />',
                obj.profile_picture.url,
            )
        return "No picture"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("user").annotate(
            posts_count=Count("posts", distinct=True)
        )


# ---------------------------------------------------------------------------
# Post
# ---------------------------------------------------------------------------


class PostAdminForm(forms.ModelForm):
    likes = forms.ModelMultipleChoiceField(
        queryset=Profile.objects.all(),
        widget=FilteredSelectMultiple("likes", is_stacked=False),
        required=False,
    )

    class Meta:
        model = Post
        fields = "__all__"

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "short_caption",
        "images_count",
        "likes_count_display",
        "comments_count",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active", "created_at", "user")
    search_fields = (
        "caption",
        "user__username",
        "user__user__username",
        "user__user__email",
    )
    # autocomplete_fields = ("user", "likes")
    # filter_horizontal = ("likes",)
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    form = PostAdminForm
    list_per_page = 25
    list_select_related = ("user",)

    fieldsets = (
        (
            None,
            {
                "fields": ("user", "caption"),
            },
        ),
        (
            "Status",
            {
                "fields": ("is_active", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    inlines = [ImageInline, CommentInline]

    @admin.display(description="Caption")
    def short_caption(self, obj):
        return (
            (obj.caption[:60] + "…") if len(obj.caption) > 60 else (obj.caption or "—")
        )

    @admin.display(description="Images", ordering="images_count")
    def images_count(self, obj):
        return getattr(obj, "images_count", obj.images.count())

    @admin.display(description="Likes", ordering="likes_count")
    def likes_count_display(self, obj):
        return getattr(obj, "likes_count", obj.likes.count())

    @admin.display(description="Comments", ordering="comments_count")
    def comments_count(self, obj):
        return getattr(obj, "comments_count", obj.comments.count())

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("user__user").annotate(
            images_count=Count("images", distinct=True),
            likes_count=Count("likes", distinct=True),
            comments_count=Count("comments", distinct=True),
        )


# ---------------------------------------------------------------------------
# Image
# ---------------------------------------------------------------------------


@admin.register(Images)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "preview", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("post__caption", "post__user__username")
    autocomplete_fields = ("post",)
    readonly_fields = ("preview", "created_at", "updated_at")
    ordering = ("-created_at",)
    list_per_page = 30
    list_select_related = ("post",)

    @admin.display(description="Preview")
    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:80px;border-radius:6px;" />',
                obj.image.url,
            )
        return "—"


# ---------------------------------------------------------------------------
# Comment
# ---------------------------------------------------------------------------


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "post", "short_text", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("text", "user__username", "post__caption", "post__user__username")
    autocomplete_fields = ("user", "post")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    list_per_page = 30
    list_select_related = ("user", "post")

    @admin.display(description="Comment")
    def short_text(self, obj):
        return (obj.text[:80] + "…") if len(obj.text) > 80 else obj.text


@admin.register(Likes)
class LikesAdmin(admin.ModelAdmin):
    model = Likes
    fields = [
        "user",
        "post",
    ]