from .models import UserAdmin, UserClient
from rest_framework import serializers

class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAdmin
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

    def create(self, validated_data):
        UserAdmin = UserAdmin.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
            # date_save ñ precisa ser passado em create
        )
        return UserAdmin

class UserClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserClient
        fields = [
            'id',
            'user',
            'client_name',
            'client_email',
            'date_save',
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8}
        }

    def create(self, validated_data):
        UserClient = UserClient.objects.create_user(
            user=validated_data['user'],
            client_name=validated_data['client_name'],
            client_email=validated_data['client_email'],
            password=validated_data['password']
        )
        return UserClient