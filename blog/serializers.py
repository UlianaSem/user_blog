from rest_framework import serializers

from blog import models


class PostCreateSerializer(serializers.ModelSerializer):
    text = serializers.CharField(required=False, max_length=140)

    class Meta:
        model = models.Post
        fields = [
            'title',
            'text'
        ]


class SubscriptionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Subscription
        fields = [
            'blog'
        ]


class PostUserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Subscription
        fields = [
            'post'
        ]
