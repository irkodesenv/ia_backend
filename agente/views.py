from rest_framework.response import Response
from .models import Agente, Instrucao, PermissaoAgenteEmpresa
from .serializers import AgenteSerializer, InstrucaoSerializer, PermissaoAgenteEmpresaSerializer
from rest_framework import viewsets
from rest_framework.decorators import action


class AgenteViewSet(viewsets.ModelViewSet):
    queryset = Agente.objects.all()
    serializer_class = AgenteSerializer
    
    @action(detail=True, methods=['get'])
    def instrucoes(self, request, pk=None):
        agente = self.get_object()
        serializer = InstrucaoSerializer(agente.instrucoes.all(), many = True)
        return Response(serializer.data)
    
    
class InstrucaoViewSet(viewsets.ModelViewSet):
    queryset = Instrucao.objects.all()
    serializer_class = InstrucaoSerializer
 

