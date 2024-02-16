from drf_spectacular import utils
from rest_framework import generics

from blog import models, permissions, paginators
from blog import serializers

parameter = utils.OpenApiParameter(
    name='Authorization',
    location=utils.OpenApiParameter.HEADER,
    description='Токен авторизации в формате Bearer <token>',
    required=True,
    type=str)


@utils.extend_schema(
    tags=["Посты"],
    parameters=[parameter],
    summary="Создать пост",
)
class PostCreateAPIView(generics.CreateAPIView):
    """Эндпоинт для создания поста"""
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostCreateSerializer

    def perform_create(self, serializer):
        post = serializer.save()
        post.blog = self.request.user.blog
        post.save()


@utils.extend_schema(
    tags=["Посты"],
    parameters=[parameter],
    summary="Удалить пост",
)
class PostDestroyAPIView(generics.DestroyAPIView):
    """Эндпоинт для удаления поста"""
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostCreateSerializer
    permission_classes = [permissions.IsBlogOwner]


@utils.extend_schema(
    tags=["Лента"],
    parameters=[parameter],
    summary="Получить ленту новостей",
)
class PostListAPIView(generics.ListAPIView):
    """Эндпоинт ленты новостей"""
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    pagination_class = paginators.PostsPaginator

    def get_queryset(self):
        blogs_id = [subscription.blog.id for subscription in self.request.user.subscriptions.all()]

        queryset = super().get_queryset()
        queryset = queryset.filter(blog__in=blogs_id).order_by('-created_at')[:500]

        return queryset


@utils.extend_schema(
    tags=["Подписки"],
    parameters=[parameter],
    summary="Создать подписку",
)
class SubscriptionCreateAPIView(generics.CreateAPIView):
    """Эндпоинт для создания подписки"""
    queryset = models.Subscription.objects.all()
    serializer_class = serializers.SubscriptionCreateSerializer

    def perform_create(self, serializer):
        subscription = serializer.save()
        subscription.user = self.request.user
        subscription.save()


@utils.extend_schema(
    tags=["Подписки"],
    parameters=[parameter],
    summary="Удалить подписку",
)
class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    """Эндпоинт для удаления подписки"""
    queryset = models.Subscription.objects.all()
    serializer_class = serializers.SubscriptionCreateSerializer
    permission_classes = [permissions.IsOwner]


@utils.extend_schema(
    tags=["Посты"],
    parameters=[parameter],
    summary="Отметить пост прочитанным",
)
class PostUserCreateAPIView(generics.CreateAPIView):
    """Эндпоинт для выделения поста прочитанным"""
    queryset = models.PostUser.objects.all()
    serializer_class = serializers.PostUserCreateSerializer

    def perform_create(self, serializer):
        read_post = serializer.save()
        read_post.user = self.request.user
        read_post.save()


@utils.extend_schema(
    tags=["Посты"],
    parameters=[parameter],
    summary="Удалить отметку о прочтении поста",
)
class PostUserDestroyAPIView(generics.DestroyAPIView):
    """Эндпоинт для удаления признака прочитанного поста"""
    queryset = models.PostUser.objects.all()
    serializer_class = serializers.PostUserCreateSerializer
    permission_classes = [permissions.IsOwner]
