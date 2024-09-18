from rest_framework import serializers
from .models import Agente, Instrucao, PermissaoAgenteEmpresa, baseConhecimento
import json


class InstrucaoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Instrucao
        fields = (
            'id',
            'instrucao',
            'created_at',
        )
        
        
class PermissaoAgenteEmpresaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PermissaoAgenteEmpresa
        fields = (
            'id_agente',
            'id_empresa'
        )
        
        
class BaseConhecimentoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = baseConhecimento
        fields = ('id_agente', 'arquivo')


class AgenteSerializer(serializers.ModelSerializer):
    instrucoes = InstrucaoSerializer(many=True, read_only=True)
    instrucoes_data = serializers.CharField(write_only=True, required=False)
    
    base_conhecimento = BaseConhecimentoSerializer(many=True, read_only=True)
    base_conhecimento_data = serializers.ListField(
        child=serializers.FileField(max_length=None, allow_empty_file=True, use_url=False),
        write_only=True, required=False
    )
    
    class Meta:
        model = Agente
        fields = (
            'idmaster',
            'nome',
            'descritivo',
            'logo_agente',
            'max_token',
            'created_at',
            'update_at',
            'instrucoes',
            'instrucoes_data',
            'base_conhecimento',
            'base_conhecimento_data'
        )
        extra_kwargs = {
            'idmaster': {'read_only': True}
        }


    def create(self, validated_data):
        instrucoes_json = validated_data.pop('instrucoes_data', '[]')
        instrucoes_data = json.loads(instrucoes_json)
        base_conhecimento_files = validated_data.pop('base_conhecimento_data', [])        
        
        agente = Agente.objects.create(**validated_data)

        for instrucao_data in instrucoes_data:
            Instrucao.objects.create(id_agente=agente, **instrucao_data)
            
        for arquivo in base_conhecimento_files:
            baseConhecimento.objects.create(id_agente=agente, arquivo=arquivo)

        return agente

    
    def update(self, instance, validated_data):
        instrucoes_data = validated_data.pop('instrucoes', [])
        
        # Atualiza a instância do Agente
        instance.nome = validated_data.get('nome', instance.nome)
        instance.descritivo = validated_data.get('descritivo', instance.descritivo)
        instance.max_token = validated_data.get('max_token', instance.max_token)
        instance.update_at = validated_data.get('update_at', instance.update_at)
        instance.save()

        # Lida com as atualizações das instruções aninhadas
        Instrucao.objects.filter(id_agente=instance).delete()
        for instrucao_data in instrucoes_data:
            Instrucao.objects.create(id_agente=instance, **instrucao_data)

        return instance


class AgenteSerializerForChat(serializers.ModelSerializer):

    class Meta:
        model = Agente
        fields = (
            'nome',
            'descritivo',
            'max_token',
            'logo_agente'
        )