from .models import Category
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'user',
            'name',
            'type',
            'category_color',
            'description',
            'created_at',
        ]
        read_only_fields = ['user']

    def validate_account(self, value):
        user = self.context['request'].user
        if value.user != user:
            raise serializers.ValidationError("Esta conta não pertence a você.")
        return value
    
    def create(self, validated_data):
        category = Category.objects.create(**validated_data)
        return category