from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny


class AuthLogin(viewsets.ViewSet):
    permission_classes = [AllowAny]  # Permitir acesso sem autenticação

    @action(detail=False, methods=['post'], url_path='auth_user')
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful', 'status': 'ok'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)