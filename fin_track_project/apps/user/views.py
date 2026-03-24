from accounts.models import Account

from .models import Admin, Client
from .serializer import AdminSerializer, ClientSerializer

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from django_filters.rest_framework import DjangoFilterBackend

from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages

from logs.audit_logger import registrar_log
import base64

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
            password_auth = request.POST.get('password')

            try:
                if username_or_email and '@' in username_or_email:
                    user_email = Admin.objects.filter(email=username_or_email).first()
                    if not user_email:
                        messages.error(request, "Usuário ou senha inválidos.")
                        return render(request, 'apps/user/login.html')
                    user = authenticate(request, username=user_email.username, password=password_auth)
                    if user:
                        login(request, user)
                        # registrar_log(username_or_email, "LOGIN_SUCCESS", "Login com e-mail realizado")
                        messages.success(request, "Login realizado.")
                        return redirect('dashboard')
                    else:
                        # registrar_log(username_or_email, "LOGIN_FAIL", "Senha incorreta (email)")
                        messages.error(request, "Usuário ou senha inválidos.")
                        return render(request, 'apps/user/login.html')

                else:
                    user_username = Admin.objects.filter(username=username_or_email).first()
                    if not user_username:
                        # registrar_log(username_or_email, "LOGIN_FAIL", "Username não encontrado")
                        messages.error(request, "Usuário ou senha inválidos.")
                        return render(request, 'apps/user/login.html')
                    # registrar_log(username_or_email, "LOGIN", "Username encontrado")
                    user = authenticate(request, username=user_username.username, password=password_auth)
                    if user:
                        login(request, user)
                        # registrar_log(username_or_email, "LOGIN_SUCCESS", "Login com username realizado")
                        messages.success(request, "Login realizado.")
                        return redirect('dashboard')
                    else:
                        # registrar_log(username_or_email, "LOGIN_FAIL", "Senha incorreta (username)")
                        messages.error(request, "Usuário ou senha inválidos.")
                        return render(request, 'apps/user/login.html')

            except Exception as e:
                registrar_log(
                    username_or_email,
                    "LOGIN_ERROR",
                    f"Erro inesperado: {str(e)}"
                )
                messages.error(request, "Usuário ou senha inválidos.")

        return render(request, 'apps/user/login.html')
    
    @login_required
    def user_logout_view(request):
        try:
            user = request.user
            username = user.username if user.is_authenticated else "Anônimo"
            registrar_log(username, "Logout", "Usuário fez logout.")
        except Exception as e:
            registrar_log(username, "Logout", f"Erro ao registrar logout: {e}")
        if logout(request):
            messages.success(request, "Logout realizado.")
        return redirect('user:login')
    
    @login_required
    def user_password_change_view(request):
        if request.method == 'POST':
            user = request.user

            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm = request.POST.get('confirm_new_password')

            if not user.check_password(old_password):
                messages.error(request, 'Senha atual incorreta!')
                return redirect(f"{reverse('user:profile')}#senha")

            if new_password != confirm:
                messages.error(request, 'As senhas não conferem!')
                return redirect(f"{reverse('user:profile')}#senha")

            if len(new_password) < 8:
                messages.error(request, 'A senha deve ter no mínimo 8 caracteres.')
                return redirect(f"{reverse('user:profile')}#senha")

            user.set_password(new_password)
            user.save()

            update_session_auth_hash(request, user)

            messages.success(request, 'Senha alterada com sucesso!')
            return redirect('user:profile')

        return redirect(f"{reverse('user:profile')}#senha")
    
    def user_register_view(request):
        if request.method == 'POST':
            
            username = request.POST.get('client_name')
            email = request.POST.get('client_email')
            password = request.POST.get('password')
            confirmacao = request.POST.get('password_confirm')
            avatar = request.FILES.get('avatar')

            if password != confirmacao:
                messages.error(request, "As senhas não conferem!")
                return render(request, 'apps/user/register.html')

            serializer = ClientSerializer(data={
                'client_name': username,
                'client_email': email,
                'password': password,
                'avatar' : avatar
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
        avatar_base64 = None
        accounts = Account.objects.filter(user=request.user)
        active_accounts = accounts.filter(is_active=True).count()


        if user.avatar:
            # Converte o binário para base64 para o HTML
            avatar_base64 = base64.b64encode(user.avatar).decode('utf-8')

        context = {
            'user': user,
            'avatar_base64': avatar_base64,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'active_accounts': active_accounts
        }
        return render(request, 'apps/user/profile.html', context)

    @login_required
    def user_profile_update_view(request):
        if request.method == 'POST':
            user = request.user
            username = request.POST.get('username')
            email = request.POST.get('email')
            avatar_file = request.FILES.get('avatar')

            user.username = username
            user.email = email
            
            if avatar_file:
                user.avatar = avatar_file.read()
            
            user.save()

            client = getattr(user, 'clients', None)
            if client:
                client_update = user.clients.first() 
                if client_update:
                    client_update.client_name = username
                    client_update.client_email = email
                    if avatar_file:
                        client_update.avatar = user.avatar
                    client_update.save()

            messages.success(request, "Perfil atualizado com sucesso.")
            return redirect('user:profile')

        return redirect('user:profile')