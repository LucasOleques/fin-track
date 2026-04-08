from .models import Account
from .serializer import AccountSerializer

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django_filters.rest_framework import DjangoFilterBackend

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['bank', 'active', 'account_type']

    @login_required
    def accounts_list_view(request):
        accounts = Account.objects.filter(user=request.user)

        bank = request.GET.get('bank')
        if bank:
            accounts = accounts.filter(bank__icontains=bank) | accounts.filter(name__icontains=bank)

        account_type = request.GET.get('type')
        if account_type:
            accounts = accounts.filter(type=account_type)

        is_active = request.GET.get('is_active')
        if is_active:
            accounts = accounts.filter(is_active=(is_active == 'True'))

        accounts = accounts.order_by('name')
        return render(request, 'apps/accounts/list.html', {'accounts': accounts})

    @login_required
    def accounts_detail_view(request, pk):
        account = Account.objects.filter(user=request.user, pk=pk).first()

        if not account:
            messages.error(request, "Conta não encontrada.")
            return redirect('accounts:list')
        
        return render(request, 'apps/accounts/detail.html', {'account': account, 'pk': pk })

    @login_required
    def accounts_create_view(request):
        if request.method == 'POST':

            name = request.POST.get('name')
            bank = request.POST.get('bank')
            type = request.POST.get('type')
            account_color = request.POST.get('account_color')
            balance = request.POST.get('balance')
            credit_limit = request.POST.get('credit_limit')
            is_active = request.POST.get('is_active')

            serializer = AccountSerializer(data={
                'name': name,
                'bank': bank,
                'type': type,
                'account_color': account_color,
                'balance' : balance,
                'credit_limit': credit_limit,
                'is_active': is_active,
            })
            
            if serializer.is_valid():
                serializer.save(user=request.user)
                messages.success(request, "Conta cadastrada.")
                return redirect('accounts:create')
            else:
                for field_errors in serializer.errors.values():
                    for error in field_errors:
                        messages.error(request, error)
        return render(request, 'apps/accounts/create.html')

    @login_required
    def accounts_edit_view(request, pk):
        account = Account.objects.filter(user=request.user, pk=pk).first()

        if not account:
            messages.error(request, "Conta não encontrada.")
            return redirect('accounts:list')

        if request.method == 'POST':
            data = {
                'name': request.POST.get('name'),
                'bank': request.POST.get('bank'),
                'type': request.POST.get('type'),
                'account_color': request.POST.get('account_color'),
                'balance': request.POST.get('balance'),
                'credit_limit': request.POST.get('credit_limit') or 0,
                'is_active': request.POST.get('is_active') == 'on',
            }

            serializer = AccountSerializer(account, data=data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                messages.success(request, f"Conta '{account.name}' atualizada com sucesso!")
                return redirect('accounts:list')
            else:
                for field, errors in serializer.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")

        return render(request, 'apps/accounts/edit.html', {'account': account})

    @login_required
    def accounts_delete_view(request, pk):
        account = Account.objects.filter(user=request.user, pk=pk).first()

        if not account:
            messages.error(request, "Conta não encontrada.")
            return redirect('accounts:list')

        if request.method == 'POST':
            try:
                account.delete()
                messages.success(request, "Conta excluída com sucesso!")
            except Exception as e:
                messages.error(request, f"Erro ao excluir a conta: {str(e)}")
            
            return redirect('accounts:list')

        return render(request, 'apps/accounts/delete.html', {'account': account})