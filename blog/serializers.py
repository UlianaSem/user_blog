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


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Post
        fields = "__all__"


class SubscriptionCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = models.Subscription
        fields = [
            'blog',
            'user'
        ]
        validators = [
            serializers.UniqueTogetherValidator(
                models.Subscription.objects.all(),
                ['user', 'blog'],
                'Вы уже подписаны на этот блог')
        ]


class PostUserCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = models.PostUser
        fields = [
            'post'
            'user'
        ]
        validators = [
            serializers.UniqueTogetherValidator(
                models.PostUser.objects.all(),
                ['user', 'post'],
                'Вы уже отметили на этот пост прочитанным')
        ]
