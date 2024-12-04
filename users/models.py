from django.db import models

from django.contrib.auth.models import AbstractUser

from users.validators import phone_validator

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    username = None

    phone = models.CharField(max_length=16, unique=True, verbose_name='Телефон',
                             help_text='Введите номер телефона в формате 79997776655', validators=[phone_validator])
    name = models.CharField(max_length=50, verbose_name='Имя', help_text='Введите имя', **NULLABLE)
    last_name = models.CharField(max_length=50, verbose_name='Фамилия', help_text='Введите фамилию', **NULLABLE)
    invite_code = models.CharField(max_length=6, unique=True, verbose_name='Инвайт-код')
    activated_invite_code = models.CharField(max_length=6, verbose_name='Активированный инвайт-код', **NULLABLE)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.phone
