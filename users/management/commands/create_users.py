from django.core.management import BaseCommand
from django.db import IntegrityError

from users import models


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            for index in range(150):
                user = models.User(email=f'test{index}@test.ru')
                user.set_password(f'test{index}')
                user.save()
        except IntegrityError:
            pass
