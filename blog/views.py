from rest_framework import generics

from blog import models, permissions
from blog import serializers


class PostCreateAPIView(generics.CreateAPIView):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostCreateSerializer

    def perform_create(self, serializer):
        post = serializer.save()
        post.blog = self.request.user.blog
        post.save()


class PostDestroyAPIView(generics.DestroyAPIView):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostCreateSerializer
    permission_classes = [permissions.IsBlogOwner]
