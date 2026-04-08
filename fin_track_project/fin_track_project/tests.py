from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import Account
from accounts.tests import AccountViewsTests
from categories.models import Category
from categories.tests import CategoryViewsTests
from transactions.models import Transaction
from transactions.tests import TransactionViewsTests
from user.tests import UserViewsTests


User = get_user_model()


class CoreViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="lucas",
            email="lucas@example.com",
            password="SenhaForte123",
            first_name="Lucas",
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
            balance=Decimal("300.00"),
            credit_limit=Decimal("0.00"),
            is_active=True,
        )
        cls.inactive_account = Account.objects.create(
            user=cls.user,
            name="Conta Secundaria",
            bank="Banco Verde",
            type="cartao",
            account_color="warning",
            balance=Decimal("50.00"),
            credit_limit=Decimal("200.00"),
            is_active=False,
        )
        cls.other_account = Account.objects.create(
            user=cls.other_user,
            name="Conta Externa",
            bank="Banco Externo",
            type="corrente",
            account_color="info",
            balance=Decimal("999.00"),
            credit_limit=Decimal("0.00"),
            is_active=True,
        )

        cls.salary_category = Category.objects.create(
            user=cls.user,
            name="Salario",
            type="receita",
            category_color="success",
            description="Receita principal",
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
            type="receita",
            category_color="primary",
            description="Nao deve afetar o dashboard",
        )

        today = timezone.localdate()
        cls.current_income = Transaction.objects.create(
            user=cls.user,
            account=cls.account,
            category=cls.salary_category,
            transaction_type="receita",
            value=Decimal("120.00"),
            description="Recebimento mensal",
            date=today,
        )
        cls.current_expense = Transaction.objects.create(
            user=cls.user,
            account=cls.account,
            category=cls.food_category,
            transaction_type="despesa",
            value=Decimal("45.00"),
            description="Mercado do mes",
            date=today - timedelta(days=1),
        )
        cls.previous_month_transaction = Transaction.objects.create(
            user=cls.user,
            account=cls.account,
            category=cls.salary_category,
            transaction_type="receita",
            value=Decimal("999.00"),
            description="Receita antiga",
            date=today - timedelta(days=40),
        )
        cls.other_user_transaction = Transaction.objects.create(
            user=cls.other_user,
            account=cls.other_account,
            category=cls.other_category,
            transaction_type="receita",
            value=Decimal("777.00"),
            description="Transacao externa",
            date=today,
        )

        cls.account.refresh_from_db()

    def test_base_view_renders_login_template_for_anonymous_users(self):
        response = self.client.get(reverse("base"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "apps/user/login.html")

    def test_base_view_renders_dashboard_summary_for_authenticated_users(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("base"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard.html")
        self.assertEqual(response.context["total_balance"], Decimal("1424.00"))
        self.assertEqual(response.context["active_accounts"], 1)
        self.assertEqual(response.context["monthly_income"], 0)
        self.assertEqual(response.context["monthly_expenses"], 0)
        self.assertContains(response, "Conta Principal")
        self.assertNotContains(response, "Conta Externa")

    def test_dashboard_view_requires_authentication(self):
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("next=", response.url)

    def test_dashboard_view_returns_monthly_totals_and_recent_transactions(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard.html")
        self.assertEqual(response.context["total_balance"], Decimal("1424.00"))
        self.assertEqual(response.context["active_accounts"], 1)
        self.assertEqual(response.context["monthly_income"], Decimal("120.00"))
        self.assertEqual(response.context["monthly_expenses"], Decimal("45.00"))
        self.assertEqual(
            list(response.context["transactions"]),
            [
                self.current_income,
                self.current_expense,
                self.previous_month_transaction,
            ],
        )
        self.assertContains(response, "Recebimento mensal")
        self.assertContains(response, "Mercado do mes")
        self.assertContains(response, "Receita antiga")
        self.assertNotContains(response, "Transacao externa")

    def test_footer_view_renders_existing_component_template(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("footer"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "components/footer.html")
        self.assertContains(response, "Controle financeiro simplificado")

    def test_navbar_view_renders_existing_component_template(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("navbar"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "components/navbar.html")
        self.assertContains(response, "FinTrack")
        self.assertContains(response, "Lucas")

    def test_pagination_view_renders_existing_component_template(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("pagination"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "components/pagination.html")
