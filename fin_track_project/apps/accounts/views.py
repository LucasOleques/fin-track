from rest_framework import viewsets
from .models import Account
from .serializer import AccountSerializer
from django_filters.rest_framework import DjangoFilterBackend

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name_bank', 'status', 'category'] # Neste campo coloque somente.