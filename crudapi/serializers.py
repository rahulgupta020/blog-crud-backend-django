from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BlogPost
from datetime import datetime


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class BlogPostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    timestamp = serializers.DateTimeField(read_only=True)

    class Meta:
        model = BlogPost
        fields = ('id', 'title', 'content', 'author', 'timestamp')

    def create(self, validated_data):
        author_username = validated_data.pop('author')
        author = User.objects.get(username=author_username)
        blog_post = BlogPost.objects.create(author=author, **validated_data)
        return blog_post