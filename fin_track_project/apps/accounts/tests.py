from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Account


User = get_user_model()


class AccountViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="lucas",
            email="lucas@example.com",
            password="SenhaForte123",
        )
        cls.other_user = User.objects.create_user(
            username="maria",
            email="maria@example.com",
            password="SenhaForte123",
        )

        cls.primary_account = Account.objects.create(
            user=cls.user,
            name="Conta Principal",
            bank="Banco Azul",
            type="corrente",
            account_color="primary",
            balance=Decimal("1500.00"),
            credit_limit=Decimal("0.00"),
            is_active=True,
        )
        cls.savings_account = Account.objects.create(
            user=cls.user,
            name="Poupanca Reserva",
            bank="Banco Verde",
            type="poupanca",
            account_color="success",
            balance=Decimal("320.00"),
            credit_limit=Decimal("0.00"),
            is_active=True,
        )
        cls.inactive_account = Account.objects.create(
            user=cls.user,
            name="Cartao Antigo",
            bank="Banco Azul",
            type="cartao",
            account_color="danger",
            balance=Decimal("0.00"),
            credit_limit=Decimal("1000.00"),
            is_active=False,
        )
        cls.other_account = Account.objects.create(
            user=cls.other_user,
            name="Conta de Outro Usuario",
            bank="Banco Externo",
            type="corrente",
            account_color="secondary",
            balance=Decimal("900.00"),
            credit_limit=Decimal("0.00"),
            is_active=True,
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_accounts_list_requires_authentication(self):
        self.client.logout()

        response = self.client.get(reverse("accounts:list"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("next=", response.url)

    def test_accounts_list_filters_by_search_type_and_status(self):
        response = self.client.get(
            reverse("accounts:list"),
            {
                "bank": "Principal",
                "type": "corrente",
                "is_active": "True",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "apps/accounts/list.html")
        self.assertEqual(list(response.context["accounts"]), [self.primary_account])
        self.assertContains(response, "Conta Principal")
        self.assertNotContains(response, "Poupanca Reserva")
        self.assertNotContains(response, "Cartao Antigo")
        self.assertNotContains(response, "Conta de Outro Usuario")

    def test_accounts_detail_view_shows_only_owned_account(self):
        response = self.client.get(
            reverse("accounts:detail", args=[self.primary_account.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "apps/accounts/detail.html")
        self.assertEqual(response.context["account"], self.primary_account)
        self.assertContains(response, "Conta Principal")

    def test_accounts_detail_redirects_when_account_is_not_found(self):
        response = self.client.get(
            reverse("accounts:detail", args=[self.other_account.pk]),
            follow=True,
        )

        self.assertRedirects(response, reverse("accounts:list"))
        self.assertTemplateUsed(response, "apps/accounts/list.html")
        self.assertNotContains(response, "Conta de Outro Usuario")

    def test_accounts_create_view_creates_a_new_account(self):
        response = self.client.post(
            reverse("accounts:create"),
            {
                "name": "Investimentos XP",
                "bank": "XP",
                "type": "investimento",
                "account_color": "info",
                "balance": "2750.30",
                "credit_limit": "0.00",
                "is_active": "true",
            },
            follow=True,
        )

        self.assertRedirects(response, reverse("accounts:create"))
        created_account = Account.objects.get(user=self.user, name="Investimentos XP")
        self.assertEqual(created_account.bank, "XP")
        self.assertEqual(created_account.type, "investimento")
        self.assertTrue(created_account.is_active)

    def test_accounts_create_view_keeps_user_on_form_when_payload_is_invalid(self):
        response = self.client.post(
            reverse("accounts:create"),
            {
                "name": "Conta Invalida",
                "bank": "Banco sem tipo",
                "balance": "100.00",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "apps/accounts/create.html")
        self.assertFalse(
            Account.objects.filter(user=self.user, name="Conta Invalida").exists()
        )

    def test_accounts_edit_view_updates_account_fields(self):
        response = self.client.post(
            reverse("accounts:edit", args=[self.primary_account.pk]),
            {
                "name": "Conta Atualizada",
                "bank": "Banco Roxo",
                "type": "corrente",
                "account_color": "warning",
                "balance": "1800.50",
                "credit_limit": "250.00",
                "is_active": "on",
            },
            follow=True,
        )

        self.assertRedirects(response, reverse("accounts:list"))
        self.primary_account.refresh_from_db()
        self.assertEqual(self.primary_account.name, "Conta Atualizada")
        self.assertEqual(self.primary_account.bank, "Banco Roxo")
        self.assertEqual(self.primary_account.account_color, "warning")
        self.assertEqual(self.primary_account.balance, Decimal("1800.50"))
        self.assertEqual(self.primary_account.credit_limit, Decimal("250.00"))
        self.assertTrue(self.primary_account.is_active)

    def test_accounts_delete_view_removes_account(self):
        response = self.client.post(
            reverse("accounts:delete", args=[self.savings_account.pk]),
            follow=True,
        )

        self.assertRedirects(response, reverse("accounts:list"))
        self.assertFalse(
            Account.objects.filter(pk=self.savings_account.pk, user=self.user).exists()
        )
