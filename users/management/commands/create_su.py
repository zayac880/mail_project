from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = 'Создание супер-пользователя admin@admin.ru'

    def handle(self, *args, **kwargs):
        user = User.objects.create(
            email='admin@admin.ru',
            first_name='Admin',
            last_name='admin',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )

        user.set_password('123qwe')
        user.save()
        self.stdout.write(
            self.style.SUCCESS(
                f'Супер-Пользователь {user.email} создан'
            )
        )
