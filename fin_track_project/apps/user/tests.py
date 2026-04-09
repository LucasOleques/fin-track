import base64
from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.models import Account

from .models import Client
from .tokens import email_verification_token


User = get_user_model()


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="test@example.com",
)
class UserViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = "SenhaForte123"
        cls.user = User.objects.create_user(
            username="lucas",
            email="lucas@example.com",
            password=cls.password,
            first_name="Lucas",
            email_verified=True,
        )
        cls.user.avatar = b"avatar-base"
        cls.user.save(update_fields=["avatar"])

        cls.client_record = Client.objects.create(
            user=cls.user,
            client_name="Lucas",
            client_email="lucas@example.com",
            password=make_password(cls.password),
            avatar=b"avatar-base",
        )

        Account.objects.create(
            user=cls.user,
            name="Conta Principal",
            bank="Banco Azul",
            type="corrente",
            account_color="primary",
            balance="100.00",
            credit_limit="0.00",
            is_active=True,
        )
        Account.objects.create(
            user=cls.user,
            name="Conta Inativa",
            bank="Banco Cinza",
            type="cartao",
            account_color="secondary",
            balance="0.00",
            credit_limit="500.00",
            is_active=False,
        )

    def test_login_view_renders_template(self):
        response = self.client.get(reverse("user:login"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "apps/user/login.html")
        self.assertContains(response, "FinTrack")

    def test_login_view_authenticates_with_username(self):
        response = self.client.post(
            reverse("user:login"),
            {
                "username": "lucas",
                "password": self.password,
            },
        )

        self.assertRedirects(response, reverse("dashboard"))
        self.assertEqual(self.client.session["username"], "lucas")
        self.assertEqual(self.client.session["email"], "lucas@example.com")
        self.assertTrue(self.client.session.get_expire_at_browser_close())

    def test_login_view_authenticates_with_email(self):
        response = self.client.post(
            reverse("user:login"),
            {
                "username": "lucas@example.com",
                "password": self.password,
            },
        )

        self.assertRedirects(response, reverse("dashboard"))
        self.assertEqual(self.client.session["username"], "lucas")
        self.assertEqual(self.client.session["email"], "lucas@example.com")

    def test_login_view_persists_session_when_remember_is_checked(self):
        response = self.client.post(
            reverse("user:login"),
            {
                "username": "lucas",
                "password": self.password,
                "remember": "on",
            },
        )

        self.assertRedirects(response, reverse("dashboard"))
        self.assertFalse(self.client.session.get_expire_at_browser_close())
        self.assertGreater(self.client.session.get_expiry_age(), 0)

    def test_login_view_warns_when_account_is_not_verified(self):
        User.objects.create_user(
            username="pendente",
            email="pendente@example.com",
            password="SenhaForte123",
            is_active=False,
            email_verified=False,
        )

        response = self.client.post(
            reverse("user:login"),
            {
                "username": "pendente@example.com",
                "password": "SenhaForte123",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "apps/user/login.html")
        self.assertContains(response, "Confirme seu e-mail")

    def test_login_view_returns_error_for_invalid_credentials(self):
        response = self.client.post(
            reverse("user:login"),
            {
                "username": "lucas",
                "password": "senha-errada",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "apps/user/login.html")
        self.assertContains(response, "Usuario ou senha invalidos.")

    @patch("user.views.registrar_log")
    def test_register_view_creates_inactive_user_and_sends_verification_email(
        self, mock_registrar_log
    ):
        response = self.client.post(
            reverse("user:register"),
            {
                "client_name": "Ana Souza",
                "client_email": "ana@example.com",
                "password": "OutraSenha123",
                "password_confirm": "OutraSenha123",
            },
            follow=True,
        )

        self.assertRedirects(response, reverse("user:login"))
        created_user = User.objects.get(username="Ana Souza")
        created_client = Client.objects.get(client_email="ana@example.com")
        self.assertFalse(created_user.is_active)
        self.assertFalse(created_user.email_verified)
        self.assertEqual(created_client.user, created_user)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["ana@example.com"])
        self.assertEqual(
            self.client.session.get("pending_verification_user_id"),
            created_user.pk,
        )
        self.assertEqual(response.context["pending_verification"]["email"], "ana@example.com")
        self.assertGreater(response.context["pending_verification"]["remaining_seconds"], 0)

        uidb64 = urlsafe_base64_encode(force_bytes(created_user.pk))
        token = email_verification_token.make_token(created_user)
        expected_path = reverse(
            "user:verify_email",
            kwargs={"uidb64": uidb64, "token": token},
        )
        self.assertIn(expected_path, mail.outbox[0].body)
        mock_registrar_log.assert_called()

    @patch("user.views.registrar_log")
    def test_register_view_stays_on_form_when_password_confirmation_fails(
        self, mock_registrar_log
    ):
        response = self.client.post(
            reverse("user:register"),
            {
                "client_name": "Ana Souza",
                "client_email": "ana@example.com",
                "password": "OutraSenha123",
                "password_confirm": "SenhaDiferente123",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "apps/user/register.html")
        self.assertFalse(User.objects.filter(username="Ana Souza").exists())
        mock_registrar_log.assert_not_called()

    def test_verify_email_view_activates_user_with_valid_token(self):
        pending_user = User.objects.create_user(
            username="novo",
            email="novo@example.com",
            password="SenhaForte123",
            is_active=False,
            email_verified=False,
        )

        uidb64 = urlsafe_base64_encode(force_bytes(pending_user.pk))
        token = email_verification_token.make_token(pending_user)

        response = self.client.get(
            reverse(
                "user:verify_email",
                kwargs={"uidb64": uidb64, "token": token},
            ),
            follow=True,
        )

        self.assertRedirects(response, reverse("user:login"))
        pending_user.refresh_from_db()
        self.assertTrue(pending_user.is_active)
        self.assertTrue(pending_user.email_verified)
        self.assertIsNone(self.client.session.get("pending_verification_user_id"))

    def test_verify_email_view_rejects_invalid_token(self):
        pending_user = User.objects.create_user(
            username="novo",
            email="novo@example.com",
            password="SenhaForte123",
            is_active=False,
            email_verified=False,
        )

        uidb64 = urlsafe_base64_encode(force_bytes(pending_user.pk))

        response = self.client.get(
            reverse(
                "user:verify_email",
                kwargs={"uidb64": uidb64, "token": "token-invalido"},
            ),
            follow=True,
        )

        self.assertRedirects(response, reverse("user:login"))
        pending_user.refresh_from_db()
        self.assertFalse(pending_user.is_active)
        self.assertFalse(pending_user.email_verified)

    def test_update_pending_email_view_requires_waiting_two_minutes(self):
        pending_user = User.objects.create_user(
            username="novo",
            email="novo@example.com",
            password="SenhaForte123",
            is_active=False,
            email_verified=False,
            verification_email_sent_at=timezone.now(),
        )
        Client.objects.create(
            user=pending_user,
            client_name="novo",
            client_email="novo@example.com",
            password=make_password("SenhaForte123"),
        )

        response = self.client.post(
            reverse("user:update_pending_email"),
            {
                "username": "novo@example.com",
                "password": "SenhaForte123",
                "new_email": "corrigido@example.com",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "apps/user/update_pending_email.html")
        self.assertContains(response, "A alteracao do e-mail fica disponivel 2 minutos")
        pending_user.refresh_from_db()
        self.assertEqual(pending_user.email, "novo@example.com")

    def test_update_pending_email_view_updates_email_and_resends_verification(self):
        pending_user = User.objects.create_user(
            username="novo",
            email="novo@example.com",
            password="SenhaForte123",
            is_active=False,
            email_verified=False,
            verification_email_sent_at=timezone.now() - timedelta(minutes=3),
        )
        pending_client = Client.objects.create(
            user=pending_user,
            client_name="novo",
            client_email="novo@example.com",
            password=make_password("SenhaForte123"),
        )

        response = self.client.post(
            reverse("user:update_pending_email"),
            {
                "username": "novo",
                "password": "SenhaForte123",
                "new_email": "corrigido@example.com",
            },
            follow=True,
        )

        self.assertRedirects(response, reverse("user:login"))
        pending_user.refresh_from_db()
        pending_client.refresh_from_db()
        self.assertEqual(pending_user.email, "corrigido@example.com")
        self.assertEqual(pending_client.client_email, "corrigido@example.com")
        self.assertFalse(pending_user.email_verified)
        self.assertFalse(pending_user.is_active)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["corrigido@example.com"])

    def test_profile_view_returns_user_context_and_avatar_base64(self):
        self.client.force_login(self.user)
        session = self.client.session
        session["login_time"] = "2026-04-08 08:00:00"
        session.save()

        response = self.client.get(reverse("user:profile"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "apps/user/profile.html")
        self.assertEqual(response.context["active_accounts"], 1)
        self.assertEqual(response.context["login_time"], "2026-04-08 08:00:00")
        self.assertEqual(
            response.context["avatar_base64"],
            base64.b64encode(b"avatar-base").decode("utf-8"),
        )

    def test_profile_update_view_updates_admin_and_client_records(self):
        self.client.force_login(self.user)
        avatar_file = SimpleUploadedFile(
            "avatar.png",
            b"novo-avatar",
            content_type="image/png",
        )

        response = self.client.post(
            reverse("user:profile_update"),
            {
                "username": "Lucas Silva",
                "email": "lucas.silva@example.com",
                "avatar": avatar_file,
            },
            follow=True,
        )

        self.assertRedirects(response, reverse("user:profile"))
        self.user.refresh_from_db()
        self.client_record.refresh_from_db()
        self.assertEqual(self.user.username, "Lucas Silva")
        self.assertEqual(self.user.email, "lucas.silva@example.com")
        self.assertEqual(bytes(self.user.avatar), b"novo-avatar")
        self.assertEqual(self.client_record.client_name, "Lucas Silva")
        self.assertEqual(self.client_record.client_email, "lucas.silva@example.com")
        self.assertEqual(bytes(self.client_record.avatar), b"novo-avatar")

    def test_password_change_view_rejects_invalid_current_password(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("user:password_change"),
            {
                "old_password": "senha-incorreta",
                "new_password": "NovaSenha123",
                "confirm_new_password": "NovaSenha123",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"{reverse('user:profile')}#senha")
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.password))

    def test_password_change_view_updates_password_when_payload_is_valid(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("user:password_change"),
            {
                "old_password": self.password,
                "new_password": "NovaSenha123",
                "confirm_new_password": "NovaSenha123",
            },
            follow=True,
        )

        self.assertRedirects(response, reverse("user:profile"))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("NovaSenha123"))

    @patch("user.views.registrar_log")
    def test_logout_view_clears_session_and_redirects(self, mock_registrar_log):
        self.client.force_login(self.user)
        session = self.client.session
        session["login_time"] = "2026-04-08 08:00:00"
        session.save()

        response = self.client.get(reverse("user:logout"))

        self.assertRedirects(response, reverse("user:login"))
        self.assertNotIn("_auth_user_id", self.client.session)
        mock_registrar_log.assert_called()

    def test_password_reset_view_uses_custom_template(self):
        response = self.client.get(reverse("user:password_reset"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "apps/user/password_reset.html")
