from rest_framework import serializers
from first_app.models import Account

class AccountSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    state = serializers.ReadOnlyField()
    class Meta:
        model = Account
        fields = ['id', 'image', 'name', 'game', 'description', 'price', 'user', 'state']
