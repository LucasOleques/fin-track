from .models import Admin, Client
from .serializer import AdminSerializer, ClientSerializer

from rest_framework import viewsets, renderers
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from django_filters.rest_framework import DjangoFilterBackend

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from django.http import HttpResponse

from logs.audit_logger import registrar_log

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
    
    def user_login_view(request):
        if request.method == 'POST':
            username_or_email = request.POST.get('username')
            password = request.POST.get('password')

            user = None

            if username_or_email and '@' in username_or_email:
                user_email = Admin.objects.get(email=username_or_email)
                try:
                    user = authenticate(request, username=user_email.username, password=password)

                    if user:
                        login(request, user)
                        messages.success(request, "Login realizado.")

                        registrar_log(user.username, "Login com e-mail", "Usuário fez login com e-mail.")
                        return redirect('dashboard')
                    else:
                        messages.error(request, "Senha inválida.")
                except Client.DoesNotExist:
                    messages.error(request, "Credenciais inválidas."+ str(user) + " - " + str(username_or_email))
                    pass
                
            elif username_or_email is not None:
                user_username = Admin.objects.get(username=username_or_email)
                try:
                    user = authenticate(request, username=user_username.username, password=password)

                    if user:
                        login(request, user)
                        messages.success(request, "Login realizado.")
                        registrar_log(user.username, "Login com username", "Usuário fez login com username.")
                        return redirect('dashboard')
                    
                except Client.DoesNotExist:
                    messages.error(request, "Credenciais inválidas."+ str(user) + " - " + str(username_or_email))
                    pass

            else:
                messages.error(request, "Email ou User Credenciais inválidas. " + str(user) + " - " + str(username_or_email))
                registrar_log(username_or_email, "Falha de Login", "Tentativa de login com credenciais inválidas.")

            messages.error(request, "Algo inesperado. Entre em contato com o suporte do sistema. " + str(user) + " - " + str(username_or_email))
        return render(request, 'apps/user/login.html')
    
    @login_required
    def user_logout_view(request):
        try:
            user = request.user
            username = user.username if user.is_authenticated else "Anônimo"
            registrar_log(username, "Logout", "Usuário fez logout.")
        except Exception as e:
            print(f"Erro ao registrar logout: {e}")
        if logout(request):
            messages.success(request, "Logout realizado.")
        return redirect('user:login')
    
    @login_required
    def user_password_change(request):
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Sua senha foi alterada com sucesso!')
                return redirect('user:profile')
            else:
                for field, error_list in form.errors.items():
                    for error in error_list:
                        messages.error(request, f"{error}")
        
        return redirect('user:profile')

    def user_password_reset_view(request):
        return render(request, 'apps/user/password_reset.html')
    
    def user_register_view(request):
        if request.method == 'POST':
            
            username = request.POST.get('client_name')
            email = request.POST.get('client_email')
            password = request.POST.get('password')
            confirmacao = request.POST.get('password_confirm')

            if password != confirmacao:
                messages.error(request, "As senhas não conferem!")
                return render(request, 'apps/user/register.html')

            serializer = ClientSerializer(data={
                'client_name': username,
                'client_email': email,
                'password': password
            })

            if serializer.is_valid():
                serializer.save()
                messages.success(request, "Cadastro realizado.")
                return redirect('user:login')
            else:
                for field_errors in serializer.errors.values():
                    for error in field_errors:
                        messages.error(request, error)
                        
        registrar_log(
            request.user
            if request.user.is_authenticated
            else "Anônimo", "Tentativa de Registro", "Acessou a página de registro.")
        
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
