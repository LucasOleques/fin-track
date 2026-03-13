from .models import Admin, Client
from rest_framework import serializers

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'date_save',
            'password'
            ]
        
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8}
        }

class ClientSerializer(serializers.ModelSerializer):
    client_email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'}, min_length=8)

    class Meta:
        model = Client
        fields = [
            'id_client',
            'client_name',
            'client_email',
            'password',
            'date_save',
        ]
        read_only_fields = ('id_client', 'date_save')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8}
        }
