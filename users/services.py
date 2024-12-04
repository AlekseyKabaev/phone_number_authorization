import secrets
import random
import string
import time

from smsaero import SmsAero

from users.models import User
from config.settings import SMSAERO_EMAIL, SMSAERO_API_KEY


def generate_invite_code():
    """Генерирует случайный инвайт-код, состоящий из 6 символов.

    Инвайт-код будет содержать хотя бы одну строчную букву,
    одну заглавную букву и минимум 2 цифры.
    """

    code_base = string.digits + string.ascii_letters
    while True:
        # Генерируем случайный код длиной 6 символов
        invite_code = ''.join([secrets.choice(code_base) for _ in range(6)])

        if (any(i.islower() for i in invite_code)) and (any(i.isupper() for i in invite_code)) and sum(
                i.isdigit() for i in invite_code) >= 2:
            break
    return invite_code


def create_unique_invite_code():
    """Создаёт и проверяет инвайт-код на существование среди уже существующих кодов пользователей."""
    invite_code = generate_invite_code()

    while User.objects.filter(invite_code=invite_code).exists():
        invite_code = generate_invite_code()

    return invite_code


def generate_sms_code():
    """Генерирует случайный 4-х значный код для СМС сообщения"""
    sms_code = str(random.randint(1000, 9999))
    time.sleep(2)
    print(sms_code)
    return sms_code


def send(phone: int, message: str) -> dict:
    """
    Отправляет СМС-сообщение

    Параметры:
    телефон (int): номер телефона, на который будет отправлено СМС-сообщение.
    сообщение (str): содержание СМС-сообщения, которое будет отправлено.

    Возвращается:
    dict: Словарь, содержащий ответ от SmsAero API.
    """
    api = SmsAero(SMSAERO_EMAIL, SMSAERO_API_KEY)
    return api.send(phone, message)
