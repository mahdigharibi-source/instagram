from rest_framework import serializers
from instagram.models import Profile, Post, Comment, Likes, Images


class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    profile_username = serializers.CharField(source='username')
    main_username = serializers.CharField(source='user.username')

    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'email',
            'main_username',
            'profile_username',
            'is_active',
            'bio',
            'profile_picture',
        ]


class ProfileOnlyNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'profile_username',
            'profile_picture',
        ]

    profile_username = serializers.CharField(source='username', read_only=True)


class LikeSerializer(serializers.ModelSerializer):
    user = ProfileOnlyNameSerializer(read_only=True)

    class Meta:
        model = Likes
        fields = [
            'id',
            'user',

        ]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = [
            'id',
            'image',
        ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'post',
            'text',
        ]

    user = ProfileOnlyNameSerializer(read_only=True)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'user',
            'caption',
            'likes_count',
            'likes',
            'images',
            'comments',
        ]

    comments = CommentSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    user = ProfileSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    likes = LikeSerializer(
        many=True,
        read_only=True
    )

    def get_likes_count(self, obj):
        return obj.likes.count()
