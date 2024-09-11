from rest_framework import serializers
from .models import Chat
from agente.serializers import AgenteSerializerForChat


class ChatSerializer(serializers.ModelSerializer):
    agente = AgenteSerializerForChat(source='id_agente', read_only=True)

    class Meta():
        model = Chat
        fields = (
            'idmaster',
            'id_usuario',
            'id_agente',
            'autor',
            'mensagem',
            'created_at',
            'agente'
        )