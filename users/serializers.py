from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя."""

    class Meta:
        model = User
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля пользователя с дополнительной информацией о рефералах."""

    invited_users = serializers.SerializerMethodField()  # Создаем поле invited_users, которое генерируется методом

    class Meta:
        model = User
        fields = ('id', 'phone', 'name', 'last_name', 'invite_code', 'activated_invite_code', 'invited_users')

    def get_invited_users(self, obj):
        """Метод для получения списка пользователей, которые использовали инвайт-код текущего пользователя."""

        # Фильтруем пользователей, у которых activated_invite_code совпадает с invite_code текущего объекта
        user_list = User.objects.filter(activated_invite_code=obj.invite_code)
        return [user.phone for user in user_list]
