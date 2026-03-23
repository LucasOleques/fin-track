from .models import Account
from .serializer import AccountSerializer

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django_filters.rest_framework import DjangoFilterBackend

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['bank', 'active', 'account_type']

    @login_required
    def accounts_list_view(request):
        list_accounts = Account.objects.filter(user=request.user)
        return render(request, 'apps/accounts/list.html', {'accounts': list_accounts})

    @login_required
    def accounts_detail_view(request, pk):
        detail_accounts = Account.objects.filter(user=request.user, pk=pk)
        return render(request, 'apps/accounts/detail.html', {'accounts': detail_accounts, 'pk': pk})

    @login_required
    def accounts_create_view(request):
        create_accounts = Account.objects.filter(user=request.user)
        return render(request, 'apps/accounts/create.html', {'accounts': create_accounts})

    @login_required
    def accounts_edit_view(request, pk):
        edit_accounts = Account.objects.filter(user=request.user, pk=pk)
        return render(request, 'apps/accounts/edit.html', {'accounts': edit_accounts, 'pk': pk})

    @login_required
    def accounts_delete_view(request, pk):
        delete_accounts = Account.objects.filter(user=request.user, pk=pk)
        return render(request, 'apps/accounts/delete.html', {'accounts': delete_accounts, 'pk': pk})