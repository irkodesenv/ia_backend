from rest_framework import serializers
from .models import Agente, Instrucao, PermissaoAgenteEmpresa


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


class AgenteSerializer(serializers.ModelSerializer):
    instrucoes = InstrucaoSerializer(many=True)

    class Meta:
        model = Agente
        fields = (
            'idmaster',
            'nome',
            'descritivo',
            'max_token',
            'created_at',
            'update_at',
            'instrucoes'
        )
        extra_kwargs = {
            'idmaster': {'read_only': True}
        }

    def create(self, validated_data):        
        instrucoes_data = validated_data.pop('instrucoes', [])
        agente = Agente.objects.create(**validated_data)
        
        for instrucao_data in instrucoes_data:
            Instrucao.objects.create(id_agente=agente, **instrucao_data)
        
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
        )