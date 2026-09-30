from rest_framework import serializers

from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer
from instagram.models import Profile, Post, Comment, Likes



class ProfileSerializer(serializers.ModelSerializer):

    user = CustomUserSerializer(read_only=True)
    profile_username = serializers.CharField(source='username')
    main_username = serializers.CharField(source='user.username')
    class Meta:
        model = Profile
        fields = [
            'user',
            'main_username',
            'profile_username',
            'is_active',
            'bio',
            'profile_picture',
        ]

