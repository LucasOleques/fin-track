from .models import Transaction
from rest_framework import serializers

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'id',
            'user',
            'account',
            'category',
            'amount',
            'date',
            'description',
            'transaction_type',
        ]
        read_only_fields = ['user']