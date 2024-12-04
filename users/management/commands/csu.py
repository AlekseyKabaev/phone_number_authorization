from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    """Создание суперпользователя."""

    def handle(self, *args, **kwargs):
        phone = '79998887755'
        invite_code = 'Wa14ba'
        code = '1234'

        # Проверяем, существует ли пользователь с таким номером телефона
        if User.objects.filter(phone=phone).exists():
            self.stdout.write(self.style.WARNING(f'Суперпользователь с номером {phone} уже существует.'))
            return

        user = User.objects.create(phone=phone, invite_code=invite_code)

        user.set_password(code)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.stdout.write(self.style.SUCCESS(f'Суперпользователь {phone} был создан.'))
