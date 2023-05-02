from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    """Сериалайзер для регистрации."""

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError(
                'Указанный email уже существует'
            )

        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Неверное имя пользователя'
            )
        return data


class ProfileSerializer(serializers.ModelSerializer):
    """Сериалайзер для просмотра и редактирования
    пользователем своего профиля.
    """

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        read_only_fields = ('role',)


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для просмотра и редактирования пользователей
    из-под аккаунта администратора.
    """

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
