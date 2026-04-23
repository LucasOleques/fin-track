from .models import Transaction
from .serializer import TransactionSerializer

from accounts.models import Account
from categories.models import Category

from fin_track_project.views import avatar_view

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django_filters.rest_framework import DjangoFilterBackend

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.db.models import Sum

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'account',
        'category',
        'date',
        'transaction_type'
        ]


    @login_required
    def transactions_form_view(request):
        avatar_base64 = avatar_view(request)
        form_transactions = Transaction.objects.filter(user=request.user)
        context = {
            'form_transactions': form_transactions,
            'avatar_base64': avatar_base64
        }
        return render(request, 'apps/transactions/create_edit.html', context)

    @login_required
    def transactions_list_view(request):
        avatar_base64 = avatar_view(request)
        if request.method == 'GET':
            transactions = Transaction.objects.filter(user=request.user)

            date_from = request.GET.get('date_from')
            if date_from:
                transactions = transactions.filter(date__gte=date_from)
            date_to = request.GET.get('date_to')
            if date_to:
                transactions = transactions.filter(date__lte=date_to)
            
            transaction_type = request.GET.get('transaction_type')
            if transaction_type:
                transactions = transactions.filter(transaction_type=transaction_type)
            
            account_id = request.GET.get('account')
            if account_id:
                transactions = transactions.filter(account__id_account=account_id)
            
            category_id = request.GET.get('category')
            if category_id:
                transactions = transactions.filter(category__id_category=category_id)
            
            transactions = transactions.order_by('-date', '-value')
            
            accounts = Account.objects.filter(user=request.user, is_active=True)
            categories = Category.objects.filter(user=request.user)
            
            total_receita = transactions.filter(transaction_type='receita').aggregate(total=Sum('value'))['total'] or 0
            total_despesa = transactions.filter(transaction_type='despesa').aggregate(total=Sum('value'))['total'] or 0
            
            total_balanco = Account.objects.filter(user=request.user).aggregate(total=Sum('balance'))['total'] or 0

            total_balanco = total_receita + total_despesa
            saldo = total_receita - total_despesa

            context = {
                        'transactions': transactions,
                        'total_receita': total_receita,
                        'total_despesa': total_despesa,
                        'total_balanco': total_balanco,
                        'saldo': saldo,
                        'accounts': accounts,
                        'categories': categories,
                        'avatar_base64': avatar_base64
                        }
        return render(request, 'apps/transactions/list.html', context)

    @login_required
    def transactions_create(request):
        avatar_base64 = avatar_view(request)
        if request.method == 'POST':

            account = request.POST.get('account')
            category  = request.POST.get('category')
            transaction_type = request.POST.get('transaction_type')
            value = request.POST.get('value')
            description = request.POST.get('description')
            date = request.POST.get('date')
            payment_method = request.POST.get('payment_method')
            notes = request.POST.get('notes')
            created_at = request.POST.get('created_at')

            serializer = TransactionSerializer(
                data={
                    'account': account,
                    'category': category,
                    'transaction_type': transaction_type,
                    'value': value,
                    'description': description,
                    'date': date,
                    'payment_method': payment_method,
                    'notes': notes,
                    'created_at': created_at
                },
                context={'request': request}
            )

            if serializer.is_valid():
                serializer.save(user=request.user)
                messages.success(request, "Transação criada com sucesso.")
                return redirect ('transactions:list')
            else:
                for field_errors in serializer.errors.values():
                    for error in field_errors:
                        messages.error(request, error)
        
        accounts = Account.objects.filter(user=request.user, is_active=True)
        categories = Category.objects.filter(user=request.user)

        context = {
            'accounts': accounts,
            'categories': categories,
            'avatar_base64': avatar_base64
        }
        return render(request, 'apps/transactions/create_edit.html', context)
    
    @login_required
    def transactions_edit_view(request, pk):
        avatar_base64 = avatar_view(request)
        transaction = Transaction.objects.filter(user=request.user,id_transaction=pk, account__user=request.user).first()

        if not transaction:
            messages.error(request, "Transação não encontrada.")
            return redirect('transactions:list')
        
        if request.method == 'POST':

            transaction.description = request.POST.get('description')
            transaction.value = request.POST.get('value')
            transaction.save()

            account = request.POST.get('account')
            category  = request.POST.get('category')
            transaction_type = request.POST.get('transaction_type')
            value = request.POST.get('value')
            description = request.POST.get('description')
            date = request.POST.get('date')
            payment_method = request.POST.get('payment_method')
            notes = request.POST.get('notes')
            created_at = request.POST.get('created_at')

            serializer = TransactionSerializer(
                instance=transaction,
                data={
                    'account': account,
                    'category': category,
                    'transaction_type': transaction_type,
                    'value': value,
                    'description': description,
                    'date': date,
                    'payment_method': payment_method,
                    'notes': notes,
                    'created_at': created_at
                },
                partial=True,
                context={'request': request}
            )

            if serializer.is_valid():
                serializer.save(user=request.user)
                messages.success(request, "Transação criada com sucesso.")
                return redirect ('transactions:list')
            else:
                for field_errors in serializer.errors.values():
                    for error in field_errors:
                        messages.error(request, error)
        
        accounts = Account.objects.filter(user=request.user, is_active=True)
        categories = Category.objects.filter(user=request.user)

        context = {
            'transaction': transaction,
            'accounts': accounts,
            'categories': categories,
            'avatar_base64': avatar_base64
        }
        return render(request, 'apps/transactions/create_edit.html', context)
    
    @login_required
    def transactions_delete_view(request, pk):
        avatar_base64 = avatar_view(request)
        transaction = Transaction.objects.filter(user=request.user,id_transaction=pk, account__user=request.user).first()

        if not transaction:
            messages.error(request, "Transação não encontrada.")
            return redirect('transactions:list')

        if request.method == 'POST':
            try:
                transaction.delete()
                messages.success(request, "Transação excluída com sucesso!")
            except Exception as e:
                messages.error(request, f"Erro ao excluir a transação: {str(e)}")
            
            return redirect('transactions:list')
        
        context = {
            'transaction': transaction,
            'avatar_base64': avatar_base64
            }

        return render(request, 'apps/transactions/list.html', context)