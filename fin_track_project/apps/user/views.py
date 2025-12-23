from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User
from .serializer import UserSerializer

class UserViewSet(mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = UserSerializer
    
    queryset = User.objects.all()

    @action(detail=False, methods=['get', 'put', 'patch'], url_path='user', url_name='user')
    def manage(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        elif request.method in ['PUT', 'PATCH']:
            # utiliza o serializer para alterar
            serializer = self.get_serializer(user, data=request.data, partial=request.method == 'PATCH')
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)