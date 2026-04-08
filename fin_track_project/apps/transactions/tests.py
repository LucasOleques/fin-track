from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import Account
from categories.models import Category

from .models import Transaction


User = get_user_model()


class TransactionViewsTests(TestCase):
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

        cls.account = Account.objects.create(
            user=cls.user,
            name="Conta Principal",
            bank="Banco Azul",
            type="corrente",
            account_color="primary",
            balance=Decimal("1000.00"),
            credit_limit=Decimal("0.00"),
            is_active=True,
        )
        cls.inactive_account = Account.objects.create(
            user=cls.user,
            name="Conta Inativa",
            bank="Banco Cinza",
            type="cartao",
            account_color="secondary",
            balance=Decimal("500.00"),
            credit_limit=Decimal("1000.00"),
            is_active=False,
        )
        cls.other_account = Account.objects.create(
            user=cls.other_user,
            name="Conta Externa",
            bank="Banco Externo",
            type="corrente",
            account_color="info",
            balance=Decimal("300.00"),
            credit_limit=Decimal("0.00"),
            is_active=True,
        )

        cls.salary_category = Category.objects.create(
            user=cls.user,
            name="Salario",
            type="receita",
            category_color="success",
            description="Entradas fixas",
        )
        cls.food_category = Category.objects.create(
            user=cls.user,
            name="Mercado",
            type="despesa",
            category_color="danger",
            description="Compras do mes",
        )
        cls.other_category = Category.objects.create(
            user=cls.other_user,
            name="Categoria Externa",
            type="despesa",
            category_color="primary",
            description="Nao pertence ao usuario logado",
        )

        today = timezone.localdate()
        cls.income_transaction = Transaction.objects.create(
            user=cls.user,
            account=cls.account,
            category=cls.salary_category,
            transaction_type="receita",
            value=Decimal("200.00"),
            description="Salario Abril",
            date=today,
            payment_method="pix",
            notes="Credito principal",
        )
        cls.expense_transaction = Transaction.objects.create(
            user=cls.user,
            account=cls.account,
            category=cls.food_category,
            transaction_type="despesa",
            value=Decimal("50.00"),
            description="Compra no mercado",
            date=today - timedelta(days=1),
            payment_method="cartao_debito",
            notes="Compras da semana",
        )
        cls.old_expense_transaction = Transaction.objects.create(
            user=cls.user,
            account=cls.account,
            category=cls.food_category,
            transaction_type="despesa",
            value=Decimal("15.00"),
            description="Compra antiga",
            date=today - timedelta(days=40),
            payment_method="dinheiro",
            notes="Compra do mes passado",
        )
        cls.other_transaction = Transaction.objects.create(
            user=cls.other_user,
            account=cls.other_account,
            category=cls.other_category,
            transaction_type="receita",
            value=Decimal("999.00"),
            description="Outra transacao",
            date=today,
            payment_method="pix",
            notes="Nao deve aparecer",
        )

        cls.account.refresh_from_db()

    def setUp(self):
        self.client.force_login(self.user)

    def test_transactions_list_requires_authentication(self):
        self.client.logout()

        response = self.client.get(reverse("transactions:list"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("next=", response.url)

    def test_transactions_form_view_lists_only_logged_user_transactions(self):
        response = self.client.get(reverse("transactions:form"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "apps/transactions/create_edit.html")
        self.assertEqual(
            set(response.context["form_transactions"]),
            {
                self.income_transaction,
                self.expense_transaction,
                self.old_expense_transaction,
            },
        )

    def test_transactions_list_view_returns_summary_for_logged_user(self):
        response = self.client.get(reverse("transactions:list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "apps/transactions/list.html")
        self.assertContains(response, "Salario Abril")
        self.assertContains(response, "Compra no mercado")
        self.assertContains(response, "Compra antiga")
        self.assertNotContains(response, "Outra transacao")
        self.assertEqual(response.context["total_receita"], Decimal("200.00"))
        self.assertEqual(response.context["total_despesa"], Decimal("65.00"))
        self.assertEqual(response.context["total_balanco"], Decimal("265.00"))
        self.assertEqual(response.context["saldo"], Decimal("135.00"))
        self.assertEqual(list(response.context["accounts"]), [self.account])
        self.assertEqual(
            set(response.context["categories"]),
            {self.salary_category, self.food_category},
        )

    def test_transactions_list_view_applies_combined_filters(self):
        date_from = (timezone.localdate() - timedelta(days=2)).isoformat()
        date_to = timezone.localdate().isoformat()

        response = self.client.get(
            reverse("transactions:list"),
            {
                "date_from": date_from,
                "date_to": date_to,
                "transaction_type": "despesa",
                "account": str(self.account.pk),
                "category": str(self.food_category.pk),
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["transactions"]), [self.expense_transaction])
        self.assertContains(response, "Compra no mercado")
        self.assertNotContains(response, "Salario Abril")
        self.assertNotContains(response, "Compra antiga")

    def test_transactions_create_view_get_shows_only_active_accounts(self):
        response = self.client.get(reverse("transactions:create"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "apps/transactions/create_edit.html")
        self.assertEqual(list(response.context["accounts"]), [self.account])
        self.assertEqual(
            set(response.context["categories"]),
            {self.salary_category, self.food_category},
        )

    def test_transactions_create_view_creates_transaction_and_updates_balance(self):
        response = self.client.post(
            reverse("transactions:create"),
            {
                "account": str(self.account.pk),
                "category": str(self.salary_category.pk),
                "transaction_type": "receita",
                "value": "120.00",
                "description": "Freelance",
                "date": timezone.localdate().isoformat(),
                "payment_method": "pix",
                "notes": "Projeto extra",
            },
            follow=True,
        )

        self.assertRedirects(response, reverse("transactions:list"))
        created_transaction = Transaction.objects.get(
            user=self.user,
            description="Freelance",
        )
        self.assertEqual(created_transaction.value, Decimal("120.00"))
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal("1255.00"))

    def test_transactions_create_view_rejects_account_from_another_user(self):
        initial_count = Transaction.objects.count()

        response = self.client.post(
            reverse("transactions:create"),
            {
                "account": str(self.other_account.pk),
                "category": str(self.food_category.pk),
                "transaction_type": "despesa",
                "value": "33.00",
                "description": "Tentativa invalida",
                "date": timezone.localdate().isoformat(),
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "apps/transactions/create_edit.html")
        self.assertEqual(Transaction.objects.count(), initial_count)
        self.assertFalse(
            Transaction.objects.filter(description="Tentativa invalida").exists()
        )

    def test_transactions_edit_view_updates_transaction_fields(self):
        response = self.client.post(
            reverse("transactions:edit", args=[self.expense_transaction.pk]),
            {
                "account": str(self.account.pk),
                "category": str(self.food_category.pk),
                "transaction_type": "despesa",
                "value": "75.00",
                "description": "Mercado da semana",
                "date": self.expense_transaction.date.isoformat(),
                "payment_method": "pix",
                "notes": "Atualizado",
            },
            follow=True,
        )

        self.assertRedirects(response, reverse("transactions:list"))
        self.expense_transaction.refresh_from_db()
        self.assertEqual(self.expense_transaction.description, "Mercado da semana")
        self.assertEqual(self.expense_transaction.value, Decimal("75.00"))

    def test_transactions_delete_view_removes_transaction_and_restores_balance(self):
        response = self.client.post(
            reverse("transactions:delete", args=[self.expense_transaction.pk]),
            follow=True,
        )

        self.assertRedirects(response, reverse("transactions:list"))
        self.assertFalse(
            Transaction.objects.filter(pk=self.expense_transaction.pk).exists()
        )
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal("1185.00"))
