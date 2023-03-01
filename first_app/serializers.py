from rest_framework import serializers
from django.http import Http404
from .auth_tools import AuthTools
from .models import TelegramUser


class TelegramUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField()
    password = serializers.CharField()
    telegram_id = serializers.IntegerField()
    class Meta:
        model = TelegramUser
        fields = ('username', 'password', 'telegram_id')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        user = AuthTools.authenticate(validated_data['username'], validated_data['password'])
        if user is not None:
            return TelegramUser.objects.create(user=user, telegram_id=validated_data['telegram_id'])
        return Http404