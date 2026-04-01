from .models import Category
from .serializer import CategorySerializer

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django_filters.rest_framework import DjangoFilterBackend

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']

    @login_required
    def categories_list_view(request):
        categories = Category.objects.filter(user=request.user)
        return render(request, 'apps/categories/list.html', {'categories': categories})

    @login_required
    def categories_create_view(request):
        if request.method == 'POST':

            name = request.POST.get('name')
            type = request.POST.get('type')
            category_color = request.POST.get('category_color')
            description = request.POST.get('description')

            serializer = CategorySerializer(data={
                'name': name,
                'type': type,
                'category_color': category_color,
                'description': description,
            })
            
            
            if serializer.is_valid():
                serializer.save(user=request.user)
                messages.success(request, "Categoria cadastrada.")
                return redirect('categories:create')
            else:
                for field_errors in serializer.errors.values():
                    for error in field_errors:
                        messages.error(request, error)

        context = {
            'category_color': Category.CATEGORY_COLOR
        }
        return render(request, 'apps/categories/create_edit.html', context)
    
    @login_required
    def categories_edit_view(request, pk):
        category = Category.objects.filter(user=request.user, id_category=pk).first()
        
        if not category:
            messages.error(request, "Categoria não encontrada.")
            return redirect('categories:list')

        if request.method == 'POST':
            name = request.POST.get('name')
            type = request.POST.get('type')
            category_color = request.POST.get('category_color')
            description = request.POST.get('description')

            serializer = CategorySerializer(category, data={
                'name': name,
                'type': type,
                'category_color': category_color,
                'description': description,
            }, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                messages.success(request, "Categoria atualizada com sucesso!")
                return redirect('categories:list')
            else:
                for field_errors in serializer.errors.values():
                    for error in field_errors:
                        messages.error(request, error)

        context = {
            'category': category,
            'category_color': Category.CATEGORY_COLOR
        }
        return render(request, 'apps/categories/create_edit.html', context)


    @login_required
    def categories_delete_view(request, pk):
        category = Category.objects.filter(user=request.user, id_category=pk).first()

        if not category:
            messages.error(request, "Categoria não encontrada.")
            return redirect('categories:list')

        if request.method == 'POST':
            try:
                category.delete()
                messages.success(request, "Categoria excluída com sucesso!")
            except Exception as e:
                messages.error(request, f"Erro ao excluir a categoria: {str(e)}")
            
            return redirect('categories:list')

        return render(request, 'apps/categories/delete.html', {'category': category})