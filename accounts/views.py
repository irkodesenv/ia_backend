from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt

import requests
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings


class AuthLogin(viewsets.ViewSet):
    permission_classes = [AllowAny]  # Permitir acesso sem autenticação


    @action(detail=False, methods=['post'], url_path='auth_user')
    @csrf_exempt
    def login(self, request):
        print("exempt_tester")
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful', 'status': 'ok'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        
        

class CustomTokenObtainPairView(TokenObtainPairView):
    
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        # Chame o microserviço de autenticação no AD
        ad_service_url = 'http://10.11.100.122:8002/api/login/'  # Substitua pela URL do microserviço
        ad_payload = {
            'username': username,
            'password': password
        }
        
        print(ad_payload)
        
        # Fazendo a requisição para o microserviço
        ad_response = requests.post(ad_service_url, ad_payload)

        # Verificar a resposta do microserviço
        if ad_response.status_code == 200:
            user_data = ad_response.json()
            from django.contrib.auth.models import User
            user, created = User.objects.get_or_create(username=user_data['username'])
            
            # Gerar tokens JWT para o usuário
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        else:
            # Autenticação falhou no microserviço
            return Response({'detail': 'Credenciais inválidas ou falha no serviço de autenticação'}, status=status.HTTP_401_UNAUTHORIZED)
