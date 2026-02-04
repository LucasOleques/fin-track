from .models import UserAdmin, UserClient
from .serializer import UserAdminSerializer, UserClientSerializer

from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from django_filters.rest_framework import DjangoFilterBackend

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout as Logout

# Web Views
def user_register_view(request):
    return render(request, 'apps/user/register.html')

@login_required
def user_profile_view(request):
    if not request.user.is_authenticated:
        return render(request, 'apps/user/profile.html', {'error': 'Usuário não autenticado.'})
    user = request.user
    context = {
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }
    return render(request, 'apps/user/profile.html', context)

def user_password_reset_view(request):
    return redirect('user:login')
    # return render(request, 'apps/user/password_reset.html')

def user_logout_view(request):
    Logout(request)
    return redirect('user:login')

def user_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if not request.POST.get('remember'):
                request.session.set_expiry(0)
            return redirect('accounts:list')
    else:
        form = AuthenticationForm()
    return render(request, 'apps/user/login.html', {'form': form})

# API ViewSets
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

# API ViewSets
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