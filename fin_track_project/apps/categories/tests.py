from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Category


User = get_user_model()


class CategoryViewsTests(TestCase):
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

        cls.expense_category = Category.objects.create(
            user=cls.user,
            name="Alimentacao",
            type="despesa",
            category_color="danger",
            description="Gastos com mercado e restaurantes",
        )
        cls.income_category = Category.objects.create(
            user=cls.user,
            name="Salario",
            type="receita",
            category_color="success",
            description="Entradas mensais",
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_categories_list_requires_authentication(self):
        self.client.logout()

        response = self.client.get(reverse("categories:list"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("next=", response.url)

    def test_categories_list_shows_only_categories_from_logged_user(self):
        response = self.client.get(reverse("categories:list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "apps/categories/list.html")
        self.assertContains(response, "Alimentacao")
        self.assertContains(response, "Salario")
        self.assertNotContains(response, "Categoria Externa")
        self.assertEqual(
            set(response.context["categories"]),
            {self.expense_category, self.income_category},
        )

    def test_categories_create_view_exposes_available_colors(self):
        response = self.client.get(reverse("categories:create"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "apps/categories/create_edit.html")
        self.assertEqual(response.context["category_color"], Category.CATEGORY_COLOR)

    def test_categories_create_view_creates_a_category(self):
        response = self.client.post(
            reverse("categories:create"),
            {
                "name": "Lazer",
                "type": "despesa",
                "category_color": "primary",
                "description": "Cinema e passeios",
            },
            follow=True,
        )

        self.assertRedirects(response, reverse("categories:create"))
        created_category = Category.objects.get(user=self.user, name="Lazer")
        self.assertEqual(created_category.type, "despesa")
        self.assertEqual(created_category.category_color, "primary")

    def test_categories_create_view_keeps_user_on_form_when_payload_is_invalid(self):
        response = self.client.post(
            reverse("categories:create"),
            {
                "name": "Categoria sem dados",
                "description": "Nao possui tipo nem cor",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "apps/categories/create_edit.html")
        self.assertFalse(
            Category.objects.filter(user=self.user, name="Categoria sem dados").exists()
        )

    def test_categories_edit_view_updates_existing_category(self):
        response = self.client.post(
            reverse("categories:edit", args=[self.expense_category.pk]),
            {
                "name": "Mercado",
                "type": "despesa",
                "category_color": "success",
                "description": "Compras de casa",
            },
            follow=True,
        )

        self.assertRedirects(response, reverse("categories:list"))
        self.expense_category.refresh_from_db()
        self.assertEqual(self.expense_category.name, "Mercado")
        self.assertEqual(self.expense_category.category_color, "success")
        self.assertEqual(self.expense_category.description, "Compras de casa")

    def test_categories_edit_view_redirects_when_category_is_not_found(self):
        response = self.client.get(
            reverse("categories:edit", args=[self.other_category.pk]),
            follow=True,
        )

        self.assertRedirects(response, reverse("categories:list"))
        self.assertTemplateUsed(response, "apps/categories/list.html")
        self.assertNotContains(response, "Categoria Externa")

    def test_categories_delete_view_removes_category(self):
        response = self.client.post(
            reverse("categories:delete", args=[self.income_category.pk]),
            follow=True,
        )

        self.assertRedirects(response, reverse("categories:list"))
        self.assertFalse(
            Category.objects.filter(pk=self.income_category.pk, user=self.user).exists()
        )
