from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse

from users.models import User
from users.services import generate_invite_code


class UserTestCase(APITestCase):
    """Тестирование регистрации пользователя."""

    def setUp(self):
        self.user = User.objects.create(phone='79995554422', name='Alex', last_name='Alex', invite_code='W2b4cd')
        self.client.force_authenticate(user=self.user)

    def test_user_retrieve(self):
        """Тестирование просмотра пользователя."""
        url = reverse('users:users_retrieve', args=(self.user.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('phone'), self.user.phone
        )

    def test_user_create(self):
        """Тестирование создания пользователя."""
        url = reverse('users:login')
        data = {
            "phone": "78887776611",
            "name": "Ivan",
            "last_name": "Test",
            "invite_code": "T1w5ab",
            "password": "1234"
        }
        response = self.client.post(url, data)

        print(response.status_code)  # Печать статуса ответа
        print(response.json())  # Печать содержимого ответа для диагностики

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            User.objects.all().count(), 2
        )

    def test_user_update(self):
        """Тестирование редактирования пользователя."""
        url = reverse('users:users_update', args=(self.user.pk,))
        data = {
            "name": "Vova",
            'last_name': "Test1",
        }
        response = self.client.patch(url, data)
        data = response.json()

        print(response.status_code)  # Печать статуса ответа
        print(response.json())  # Печать содержимого ответа для диагностики

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('name'), "Vova"
        )

    def test_generate_invite_code(self):
        """Тестирование генерации кода приглашения."""
        code = generate_invite_code()
        self.assertTrue(len(code) == 6)
        self.assertTrue(any(c.islower() for c in code))
        self.assertTrue(any(c.isupper() for c in code))
        self.assertGreaterEqual(sum(c.isdigit() for c in code), 2)
