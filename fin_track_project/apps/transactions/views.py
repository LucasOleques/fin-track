from rest_framework import viewsets
from .models import Transaction
from .serializer import TransactionSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    print("Urls de transações carregando")