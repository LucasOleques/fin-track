from .models import Admin, Client
from .serializer import AdminSerializer, ClientSerializer

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from django_filters.rest_framework import DjangoFilterBackend

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout as Logout
from django.contrib import messages

# Web Views
def user_register_view(request):
    if request.method == 'POST':
        
        nome = request.POST.get('client_name')
        email = request.POST.get('client_email')
        senha = request.POST.get('password')
        confirmacao = request.POST.get('password_confirm')

        if senha != confirmacao:
            messages.error(request, "As senhas não conferem!")
            return render(request, 'apps/user/register.html')

        serializer = ClientSerializer(data={
            'user': None,
            'client_name': nome,
            'client_email': email,
            'password': senha
        })

        if serializer.is_valid():
            serializer.save()
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect('user:login')
        else:
            for field_errors in serializer.errors.values():
                for error in field_errors:
                    messages.error(request, error)

    return render(request, 'apps/user/register.html')

@login_required
def user_profile_view(request):
    user = request.user
    context = {
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }
    return render(request, 'apps/user/profile.html', context)

def user_profile_update(request):
    return render(request, 'apps/user/profile.html')

def user_password_change(request):
    return render(request, 'apps/user/profile.html')

def user_password_reset_view(request):
    return redirect('user:login')
    # return render(request, 'apps/user/password_reset.html')

def user_logout_view(request):
    Logout(request)
    return redirect('user:login')

def user_login_view(request):
    if request.method == 'POST':
        # Permite login por e-mail ou username
        data = request.POST.copy()
        username = data.get('username')

        if username and '@' in username:
            User = get_user_model()
            try:
                user = User.objects.get(email=username)
                data['username'] = user.username
            except User.DoesNotExist:
                pass

        username_or_email = AuthenticationForm(request, data=data)
        if username_or_email.is_valid():
            user = username_or_email.get_user()
            login(request, user)
            if not request.POST.get('remember'):
                request.session.set_expiry(0)
            return render(request, 'dashboard.html', {'username_or_email': username_or_email})
    else:
        username_or_email = AuthenticationForm()
    return render(request, 'apps/user/login.html', {'username_or_email': username_or_email})

# API ViewSets
class AdminViewSet(viewsets.GenericViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'username',
        'email',
        'is_active'
        ]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()

# API ViewSets
class ClientViewSet(viewsets.GenericViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'client_name',
        'client_email',
        'user__username'
        ]
    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(user=user)
    
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()