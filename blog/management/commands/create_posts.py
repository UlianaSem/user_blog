import random

from django.core.management import BaseCommand

from blog import models


class Command(BaseCommand):

    def handle(self, *args, **options):
        blogs = models.Blog.objects.all()
        counter = 0

        if not models.Post.objects.all():

            for blog in blogs:
                quantity = random.randint(1, 4)
                for index in range(quantity):
                    models.Post.objects.create(blog=blog, title=f'Test{counter}', text=f'Test {counter}')
                    counter += 1
