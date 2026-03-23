from .models import Transaction
from .serializer import TransactionSerializer

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django_filters.rest_framework import DjangoFilterBackend

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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
        form_transactions = Transaction.objects.filter(account__user=request.user)
        return render(request, 'apps/transactions/form.html', {'form_transactions': form_transactions})

    @login_required
    def transactions_list_view(request):
        if request.method == 'GET':
            list_transactions = Transaction.objects.filter(account__user=request.user)
        return render(request, 'apps/transactions/list.html', {'list_transactions': list_transactions})

    @login_required
    def transactions_create(request):
        if request.method == 'POST':
            TransactionViewSet.create(request)
        return render(request, 'apps/transactions/create.html', {'create_transactions': None})

    @login_required
    def transactions_edit_view(request, transaction_id):
        transaction_edit = Transaction.objects.get(id=transaction_id, account__user=request.user)
        if request.method == 'POST':
            TransactionViewSet.update(request, pk=transaction_id)
        return render(request, 'apps/transactions/edit.html', {'transaction_edit': transaction_edit})