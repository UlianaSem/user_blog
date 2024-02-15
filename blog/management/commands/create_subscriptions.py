import random

from django.core.management import BaseCommand
from django.db import IntegrityError

from blog import models
from users import models as users_models


class Command(BaseCommand):

    def handle(self, *args, **options):
        users = users_models.User.objects.all()
        limit = users.count()

        if not models.Subscription.objects.all():

            for user in users:
                quantity = random.randint(40, 100)
                for index in range(quantity):
                    blog_id = random.randint(1, limit)

                    if blog_id != user.id:
                        blog = models.Blog.objects.get(id=blog_id)

                        try:
                            models.Subscription.objects.create(blog=blog, user=user)
                        except IntegrityError:
                            pass
