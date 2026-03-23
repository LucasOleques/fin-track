from .models import Category
from .serializer import CategorySerializer

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django_filters.rest_framework import DjangoFilterBackend

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']

    @login_required
    def categories_list_view(request):
        list_categories = Category.objects.filter(user=request.user)
        return render(request, 'apps/categories/list.html', {'list_categories': list_categories})

    @login_required
    def categories_create_view(request):
        if request.method == 'POST':
            name = request.POST.get('name')
            if name:
                Category.objects.create(user=request.user, name=name)
        return render(request, 'apps/categories/create.html')