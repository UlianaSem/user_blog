from rest_framework import generics

from blog import models, permissions
from blog import serializers


class PostCreateAPIView(generics.CreateAPIView):
    """Эндпоинт для создания поста"""
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostCreateSerializer

    def perform_create(self, serializer):
        post = serializer.save()
        post.blog = self.request.user.blog
        post.save()


class PostDestroyAPIView(generics.DestroyAPIView):
    """Эндпоинт для удаления поста"""
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostCreateSerializer
    permission_classes = [permissions.IsBlogOwner]


class SubscriptionCreateAPIView(generics.CreateAPIView):
    """Эндпоинт для создания подписки"""
    queryset = models.Subscription.objects.all()
    serializer_class = serializers.SubscriptionCreateSerializer

    def perform_create(self, serializer):
        subscription = serializer.save()
        subscription.user = self.request.user
        subscription.save()


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    """Эндпоинт для удаления подписки"""
    queryset = models.Subscription.objects.all()
    serializer_class = serializers.SubscriptionCreateSerializer
    permission_classes = [permissions.IsOwner]


class PostUserCreateAPIView(generics.CreateAPIView):
    """Эндпоинт для выделения поста прочитанным"""
    queryset = models.PostUser.objects.all()
    serializer_class = serializers.PostUserCreateSerializer

    def perform_create(self, serializer):
        read_post = serializer.save()
        read_post.user = self.request.user
        read_post.save()


class PostUserDestroyAPIView(generics.DestroyAPIView):
    """Эндпоинт для удаления признака прочитанного поста"""
    queryset = models.PostUser.objects.all()
    serializer_class = serializers.PostUserCreateSerializer
    permission_classes = [permissions.IsOwner]
