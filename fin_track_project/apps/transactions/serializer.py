from .models import Transaction
from rest_framework import serializers

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'user',
            'account',
            'category',
            'transaction_type',
            'value',
            'description',
            'date',
            'created_at',
        ]
        read_only_fields = ['user']

    # Validação customizada, o usuário não pode criar transação para conta de outro
    def validate_account(self, value):
        user = self.context['request'].user
        if value.user != user:
            raise serializers.ValidationError("Esta conta não pertence a você.")
        return value