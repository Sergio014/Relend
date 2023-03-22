from rest_framework import serializers
from first_app.models import Product

class ProductSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    state = serializers.ReadOnlyField()
    class Meta:
        model = Product
        fields = ['id', 'image', 'name', 'game', 'description', 'price', 'user', 'state']
