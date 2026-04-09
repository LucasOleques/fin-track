from .models import Admin, Client
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.utils import timezone


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
    avatar = serializers.FileField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Client
        fields = [
            'id_client',
            'user',
            'client_name',
            'client_email',
            'password',
            'avatar',
            'date_save',
        ]
        read_only_fields = ('id_client', 'date_save', 'user')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8}
        }

    def validate_client_email(self, value):
        if Admin.objects.filter(email=value).exists():
            raise serializers.ValidationError("Um usuário com este email já existe.")
        return value

    def create(self, validated_data):
        avatar = validated_data.pop('avatar', None)
        avatar_bytes = avatar.read() if avatar else None

        admin_user = Admin.objects.create_user(
            username=validated_data['client_name'],
            email=validated_data['client_email'],
            password=validated_data['password'],
            is_active=False,
            email_verified=False,
            verification_email_sent_at=timezone.now(),
            avatar=avatar_bytes,
        )
        
        client_user = Client.objects.create(
            user=admin_user,
            client_name=validated_data['client_name'],
            client_email=validated_data['client_email'],
            password=make_password(validated_data['password']),
            avatar=avatar_bytes,
        )

        return client_user
