from .models import Account
from rest_framework import serializers

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'user',
            'account',

            'bank',
            'account_type',
            'balance',
            'active',
        ]

        read_only_fields = ['user']

    def validate_account(self, value):
        user = self.context['request'].user
        if value.user != user:
            raise serializers.ValidationError("Esta conta não pertence a você.")
        return value
