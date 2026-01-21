from rest_framework import viewsets
from .models import UserAdmin, UserClient
from .serializer import UserAdminSerializer, UserClientSerializer

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from django_filters.rest_framework import DjangoFilterBackend


class UserAdminViewSet(viewsets.GenericViewSet):
    serializer_class = UserAdminSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'username',
        'email',
        'is_active'
        ]
    
    @action(methods=['post'], detail=False, permission_classes=[IsAdminUser])
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, IsAdminUser])
    def get_queryset(self):
        return UserAdmin.objects.all() & UserClient.objects.all()

    @action(methods=['put'], detail=True, permission_classes=[IsAuthenticated, IsAdminUser])
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=['delete'], detail=True, permission_classes=[IsAuthenticated, IsAdminUser])
    def perform_destroy(self, instance):
        instance.delete()

class UserClientViewSet(viewsets.GenericViewSet):
    serializer_class = UserClientSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'client_name',
        'client_email',
        'user__username'
        ]
    
    @action(methods=['post'], detail=False, permission_classes=[AllowAny])
    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(user=user)

    @action(methods=['get'], detail=False, authentication_classes=[JWTAuthentication], permission_classes=[IsAuthenticated])
    def get_queryset(self):
        return UserClient.objects.all()
    
    @action(methods=['put'], detail=True, authentication_classes=[JWTAuthentication], permission_classes=[IsAuthenticated])
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=['delete'], detail=True, authentication_classes=[JWTAuthentication], permission_classes=[IsAuthenticated])
    def perform_destroy(self, instance):
        instance.delete()