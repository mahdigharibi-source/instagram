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


class ImageWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = [
            'image',
        ]

class ImageReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = [
            'id',
            'image',
        ]
        extra_kwargs = {
            "id": {"read_only": True},
        }

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


class PostReadSerializer(serializers.ModelSerializer):
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
    images = ImageReadSerializer(many=True, read_only=True)
    user = ProfileSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    likes = LikeSerializer(
        many=True,
        read_only=True
    )

    def get_likes_count(self, obj):
        return obj.likes.count()

class PostWriteSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False,
    )

    user = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), required=False)

    class Meta:
        model = Post
        fields = [
            "id",
            "caption",
            "images",
        ]

    def validate(self, data):
        request = self.context.get("request")
        is_partial = request and request.method == "PATCH"

        if is_partial:
            if "images" in data and not data["images"]:
                raise serializers.ValidationError(
                    {"images": "a post must have at least one image"}
                )

        else:
            if not data.get("images"):
                raise serializers.ValidationError(
                    {"images": "a post must have at least one image"}
                )

        return data

    def create(self, validated_data):
        # عکس هارو از دیکشنری خارج میکنیم تا بهمون ارور نده و بتونیم پست بسازیم
        images = validated_data.pop("images", [])
        request = self.context.get("request")
        user_profile = request.user.profile
        post = Post.objects.create(user=user_profile, **validated_data)
        Images.objects.bulk_create(
            [Images(post=post , image=img) for img in images],
        )
        return post

    def update(self, instance, validated_data):
        images = validated_data.pop("images", None)
        for attrs, value in validated_data.items():
            setattr(instance, attrs, value)

        instance.save()

        if images:
            instance.images.all().delete()
            Images.objects.bulk_create(
                [Images(post=instance, image=img) for img in images]
            )
        return instance


    def to_internal_value(self, data):
        if hasattr(data, "get") and data.get("images") == "":
            data = data.copy()
            data.setlist("images", [])
        return super().to_internal_value(data)

    def to_representation(self, instance):
        return PostReadSerializer(instance, context=self.context).data
