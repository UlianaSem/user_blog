from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.signals import post_save
from django.dispatch import receiver

from config import settings


class Blog(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
        related_name='blog'
    )

    def __str__(self):
        return f'Blog of {self.user.email} user'

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_blog(sender, instance, created, **kwargs):
    if created:
        Blog.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_blog(sender, instance, **kwargs):
    instance.blog.save()


class Post(models.Model):
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        verbose_name='блог',
        related_name='posts'
    )
    title = models.CharField(
        max_length=100,
        verbose_name='заголовок'
    )
    text = models.CharField(
        max_length=140,
        verbose_name='текст',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='время создания'
    )

    def __str__(self):
        return f'Post {self.title} from {self.created_at}'

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'


class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
        related_name='subscriptions'
    )
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        verbose_name='блог',
        related_name='subscriptions'
    )

    def __str__(self):
        return f'User {self.user.email} subscribed to {self.blog}'

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
        constraints = [
            UniqueConstraint(
                fields=('user', 'blog',),
                name='Unique user and blog', ),
        ]
