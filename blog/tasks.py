from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from users import models as users_models
from blog import models


@shared_task
def send_updated_news_feed():
    users = users_models.User.objects.filter(is_active=True).filter(is_staff=False)

    for user in users:
        blogs_id = [subscription.blog.id for subscription in user.subscriptions.all()]
        posts = models.Post.objects.filter(blog__in=blogs_id).order_by('-created_at')[:5]

        if posts:
            message = 'Посмотрите записи в ваших подписках\n'

            for post in posts:
                message += f'{post.title}\n'

            send_mail(
                subject="Обновления в новостной ленте",
                message=message,
                recipient_list=[user.email],
                from_email=settings.EMAIL_HOST_USER,
                fail_silently=False
            )
