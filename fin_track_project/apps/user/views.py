import base64
from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Count

from accounts.models import Account
from logs.audit_logger import registrar_log

from .models import Admin, Client
from .serializer import AdminSerializer, ClientSerializer
from .services import send_verification_email
from .tokens import email_verification_token


EMAIL_CHANGE_WAIT_TIME = timedelta(minutes=2)
PENDING_VERIFICATION_SESSION_KEY = "pending_verification_user_id"


def _get_user_by_identifier(username_or_email):
    if username_or_email and "@" in username_or_email:
        return Admin.objects.filter(email=username_or_email).first()
    return Admin.objects.filter(username=username_or_email).first()

def _get_verification_email_change_remaining(user):
    available_at = user.verification_email_sent_at + EMAIL_CHANGE_WAIT_TIME
    remaining = available_at - timezone.now()
    return remaining if remaining.total_seconds() > 0 else timedelta(0)

def _format_timedelta(delta):
    total_seconds = max(0, int(delta.total_seconds()))
    minutes, seconds = divmod(total_seconds, 60)
    if minutes and seconds:
        return f"{minutes} min e {seconds} s"
    if minutes:
        return f"{minutes} min"
    return f"{seconds} s"

def _store_pending_verification_state(request, user):
    request.session[PENDING_VERIFICATION_SESSION_KEY] = user.pk

def _clear_pending_verification_state(request):
    request.session.pop(PENDING_VERIFICATION_SESSION_KEY, None)

def _get_pending_verification_context(request):
    pending_user_id = request.session.get(PENDING_VERIFICATION_SESSION_KEY)
    if not pending_user_id:
        return {}

    user = Admin.objects.filter(pk=pending_user_id).first()
    if not user or user.is_active or user.email_verified:
        _clear_pending_verification_state(request)
        return {}

    remaining = _get_verification_email_change_remaining(user)

    return {
        "pending_verification": {
            "email": user.email,
            "remaining_seconds": max(0, int(remaining.total_seconds())),
            "remaining_text": _format_timedelta(remaining) if remaining else "Disponivel agora",
            "change_available": remaining.total_seconds() <= 0,
        }
    }

def _render_login(request):
    return render(
        request,
        "apps/user/login.html",
        _get_pending_verification_context(request),
    )

class AdminViewSet(viewsets.GenericViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["username", "email", "is_active"]


class ClientViewSet(viewsets.GenericViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["client_name", "client_email", "user__username"]

    def user_login_view(request):
        if request.method == "POST":
            username_or_email = request.POST.get("username")
            password_auth = request.POST.get("password")
            remember_user = request.POST.get("remember") == "on"

            try:
                user_record = _get_user_by_identifier(username_or_email)

                if not user_record or not user_record.check_password(password_auth):
                    messages.error(request, "Usuario ou senha invalidos.")
                    return _render_login(request)

                if not user_record.is_active:
                    _store_pending_verification_state(request, user_record)
                    if user_record.email_verified:
                        messages.error(
                            request,
                            "Sua conta esta inativa no momento. Entre em contato com o suporte.",
                        )
                    else:
                        remaining = _get_verification_email_change_remaining(user_record)
                        if remaining:
                            messages.warning(
                                request,
                                "Confirme seu e-mail antes de acessar a plataforma. Se precisar corrigi-lo, a alteracao sera liberada em "
                                f"{_format_timedelta(remaining)}.",
                            )
                        else:
                            messages.warning(
                                request,
                                "Confirme seu e-mail antes de acessar a plataforma. Se precisar corrigi-lo, voce ja pode usar a opcao de alterar e-mail pendente.",
                            )
                    return _render_login(request)

                user = authenticate(
                    request,
                    username=user_record.username,
                    password=password_auth,
                )
                if not user:
                    messages.error(request, "Usuario ou senha invalidos.")
                    return _render_login(request)

                login(request, user)
                _clear_pending_verification_state(request)
                request.session.set_expiry(
                    settings.SESSION_COOKIE_AGE if remember_user else 0
                )
                request.session["user_id"] = user.id
                request.session["username"] = user.username
                request.session["email"] = user.email
                request.session["login_time"] = str(timezone.now())
                messages.success(request, "Login realizado.")
                return redirect("dashboard")

            except Exception as exc:
                registrar_log(
                    username_or_email or "Anonimo",
                    "LOGIN_ERROR",
                    f"Erro inesperado: {str(exc)}",
                )
                messages.error(request, "Nao foi possivel realizar o login.")

        return _render_login(request)

    @login_required
    def user_logout_view(request):
        try:
            user = request.user
            username = user.username if user.is_authenticated else "Anonimo"
            registrar_log(username, "LOGOUT", "Usuario fez logout.")
        except Exception as exc:
            registrar_log("Anonimo", "LOGOUT_ERROR", f"Erro ao registrar logout: {exc}")

        request.session.flush()
        logout(request)
        messages.success(request, "Logout realizado.")
        return redirect("user:login")

    @login_required
    def user_password_change_view(request):
        if request.method == "POST":
            user = request.user
            old_password = request.POST.get("old_password")
            new_password = request.POST.get("new_password")
            confirm = request.POST.get("confirm_new_password")

            if not user.check_password(old_password):
                messages.error(request, "Senha atual incorreta.")
                return redirect(f"{reverse('user:profile')}#senha")

            if new_password != confirm:
                messages.error(request, "As senhas nao conferem.")
                return redirect(f"{reverse('user:profile')}#senha")

            if len(new_password) < 8:
                messages.error(request, "A senha deve ter no minimo 8 caracteres.")
                return redirect(f"{reverse('user:profile')}#senha")

            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)

            messages.success(request, "Senha alterada com sucesso.")
            return redirect("user:profile")

        return redirect(f"{reverse('user:profile')}#senha")

    def user_register_view(request):
        if request.method == "POST":
            username = request.POST.get("client_name")
            email = request.POST.get("client_email")
            password = request.POST.get("password")
            confirmacao = request.POST.get("password_confirm")
            avatar = request.FILES.get("avatar")

            if password != confirmacao:
                messages.error(request, "As senhas nao conferem.")
                return render(request, "apps/user/register.html")

            serializer = ClientSerializer(
                data={
                    "client_name": username,
                    "client_email": email,
                    "password": password,
                    "avatar": avatar,
                }
            )

            if serializer.is_valid():
                try:
                    with transaction.atomic():
                        client = serializer.save()
                        send_verification_email(request, client.user)
                        _store_pending_verification_state(request, client.user)

                    registrar_log(
                        email or "Anonimo",
                        "REGISTRO",
                        "Cadastro criado com envio de e-mail de verificacao.",
                    )
                    messages.success(
                        request,
                        "Cadastro realizado. Verifique seu e-mail para ativar a conta.",
                    )
                    return redirect("user:login")
                except Exception as exc:
                    registrar_log(
                        email or "Anonimo",
                        "REGISTRO_ERRO",
                        f"Falha ao enviar e-mail de verificacao: {str(exc)}",
                    )
                    messages.error(
                        request,
                        "Nao foi possivel concluir o cadastro agora. Tente novamente em instantes.",
                    )
            else:
                for field_errors in serializer.errors.values():
                    for error in field_errors:
                        messages.error(request, error)

        registrar_log(
            request.user if request.user.is_authenticated else "Anonimo",
            "TENTATIVA_REGISTRO",
            "Acessou a pagina de registro.",
        )
        return render(request, "apps/user/register.html")

    def user_update_pending_email_view(request):
        if request.method == "POST":
            username_or_email = request.POST.get("username")
            password_auth = request.POST.get("password")
            new_email = (request.POST.get("new_email") or "").strip()

            user_record = _get_user_by_identifier(username_or_email)

            if not user_record or not user_record.check_password(password_auth):
                messages.error(request, "Usuario ou senha invalidos.")
                return render(request, "apps/user/update_pending_email.html")

            if user_record.is_active or user_record.email_verified:
                messages.info(
                    request,
                    "Sua conta ja esta validada. Use o perfil para alterar o e-mail.",
                )
                return redirect("user:login")

            if not new_email:
                messages.error(request, "Informe o novo e-mail.")
                return render(request, "apps/user/update_pending_email.html")

            if new_email.lower() == (user_record.email or "").lower():
                messages.error(
                    request,
                    "Informe um e-mail diferente do atual para reenviar a verificacao.",
                )
                return render(request, "apps/user/update_pending_email.html")

            remaining = _get_verification_email_change_remaining(user_record)
            if remaining:
                messages.warning(
                    request,
                    "A alteracao do e-mail fica disponivel 2 minutos apos o ultimo envio. Aguarde "
                    f"{_format_timedelta(remaining)} e tente novamente.",
                )
                return render(request, "apps/user/update_pending_email.html")

            if Admin.objects.filter(email__iexact=new_email).exclude(pk=user_record.pk).exists():
                messages.error(request, "Ja existe um usuario com este e-mail.")
                return render(request, "apps/user/update_pending_email.html")

            if Client.objects.filter(client_email__iexact=new_email).exclude(user=user_record).exists():
                messages.error(request, "Ja existe um cadastro pendente com este e-mail.")
                return render(request, "apps/user/update_pending_email.html")

            try:
                with transaction.atomic():
                    user_record.email = new_email
                    user_record.email_verified = False
                    user_record.is_active = False
                    user_record.verification_email_sent_at = timezone.now()
                    user_record.save(
                        update_fields=[
                            "email",
                            "email_verified",
                            "is_active",
                            "verification_email_sent_at",
                        ]
                    )

                    client_record = user_record.clients.first()
                    if client_record:
                        client_record.client_email = new_email
                        client_record.save(update_fields=["client_email"])

                    send_verification_email(request, user_record)
                    _store_pending_verification_state(request, user_record)

                registrar_log(
                    user_record,
                    "ALTERACAO_EMAIL_PENDENTE",
                    "Usuario alterou o e-mail antes da confirmacao.",
                )
                messages.success(
                    request,
                    "E-mail atualizado com sucesso. Enviamos um novo link de verificacao.",
                )
                return redirect("user:login")
            except Exception as exc:
                registrar_log(
                    user_record,
                    "ALTERACAO_EMAIL_PENDENTE_ERRO",
                    f"Falha ao atualizar o e-mail pendente: {str(exc)}",
                )
                messages.error(
                    request,
                    "Nao foi possivel atualizar o e-mail agora. Tente novamente em instantes.",
                )

        return render(request, "apps/user/update_pending_email.html")

    def user_verify_email_view(request, uidb64, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = Admin.objects.filter(pk=user_id).first()
        except (TypeError, ValueError, OverflowError):
            user = None

        if not user or not email_verification_token.check_token(user, token):
            messages.error(
                request,
                "O link de verificacao e invalido ou expirou.",
            )
            return redirect("user:login")

        if user.email_verified and user.is_active:
            _clear_pending_verification_state(request)
            messages.info(request, "Seu e-mail ja foi confirmado. Faca login.")
            return redirect("user:login")

        user.email_verified = True
        user.is_active = True
        user.save(update_fields=["email_verified", "is_active"])
        _clear_pending_verification_state(request)

        registrar_log(user, "EMAIL_VERIFICADO", "Conta ativada com sucesso.")
        messages.success(
            request,
            "E-mail confirmado com sucesso. Agora voce ja pode entrar.",
        )
        return redirect("user:login")

    @login_required
    def user_profile_view(request):
        user = request.user
        avatar_base64 = None

        accounts_with_stats = Account.objects.filter(user=request.user).annotate(
            num_transactions=Count('transactions')
        )
        active_accounts = sum(1 for acc in accounts_with_stats if acc.is_active)
        total_transactions = sum(acc.num_transactions for acc in accounts_with_stats)

        login_time = request.session.get("login_time", "Nao disponivel")

        if user.avatar:
            avatar_base64 = base64.b64encode(user.avatar).decode("utf-8")

        context = {
            "user": user,
            "avatar_base64": avatar_base64,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "active_accounts": active_accounts,
            "total_transactions": total_transactions,   
            "login_time": login_time,
        }
        return render(request, "apps/user/profile.html", context)
 
    @login_required
    def user_profile_update_view(request):
        if request.method == "POST":
            user = request.user
            username = request.POST.get("username")
            email = request.POST.get("email")
            avatar_file = request.FILES.get("avatar")

            user.username = username
            user.email = email

            if avatar_file:
                user.avatar = avatar_file.read()

            user.save()

            client = getattr(user, "clients", None)
            if client:
                client_update = user.clients.first()
                if client_update:
                    client_update.client_name = username
                    client_update.client_email = email
                    if avatar_file:
                        client_update.avatar = user.avatar
                    client_update.save()

            messages.success(request, "Perfil atualizado com sucesso.")
            return redirect("user:profile")

        return redirect("user:profile")
