from rest_framework.response import Response
from .models import Chat
from .serializers import ChatSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.db.models import OuterRef, Subquery
import openai
from agente.models import Agente, Instrucao, baseConhecimento
from central.settings import API_OPENIA_KEY, MEDIA_ROOT
from docx import Document
import os

openai.api_key = API_OPENIA_KEY

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer    
        
        
    def get_queryset(self):
        idmaster = self.request.query_params.get('idmaster', None)
        id_usuario = self.request.query_params.get('id_usuario', None)

        if idmaster and id_usuario:
            return Chat.objects.filter(idmaster=idmaster, id_usuario=id_usuario).order_by('created_at')
            
        elif idmaster:
            return Chat.objects.filter(idmaster=idmaster).order_by('created_at')
        
        elif id_usuario:
            return Chat.objects.filter(id_usuario=id_usuario).order_by('created_at')

        #return Chat.objects.none()
        return super().get_queryset()
    
    
    @action(detail=False, methods=['delete'], url_path='deletar')
    def delete_filtered_chats(self, request):
        
        chats_to_delete = self.get_queryset()

        if chats_to_delete.exists():
            count, _ = chats_to_delete.delete()
            return Response({'message': f'{count} chats deletados com sucesso.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Nenhum chat encontrado para deletar.'}, status=status.HTTP_404_NOT_FOUND)
        
    
    @action(detail=False, methods=['get'], url_path='listaChats')
    def retorna_agentes_distinct(self, request):
        # Subquery para obter o ID do chat mais recente para cada idmaster
        subquery = Chat.objects.filter(
            id_usuario=1, 
            idmaster=OuterRef('idmaster')
        ).order_by('-created_at').values('id')[:1]

        # Consulta principal para obter os chats mais recentes
        distinct_chats = Chat.objects.filter(id__in=Subquery(subquery)).select_related('id_agente').order_by('-created_at')

        # Usando o serializer que inclui informações do agente
        serializer = ChatSerializer(distinct_chats, many=True)
        return Response(serializer.data)
    

    @action(detail=False, methods=['post'], url_path='enviarPergunta')
    def enviar_pergunta(self, request):
        data = request.data
        data_id_agente = data.get('id_agente', '')
        idmaster = data.get('idmaster')
        instancia_agente = get_object_or_404(Agente, idmaster = data_id_agente)
        data.pop('id_agente', None)        
        arr_mensagens = []    
        
        # Busca base de conhecimento
        base_conhecimento = self.obter_base_conhecimento_agente(data_id_agente)        
        if base_conhecimento:
            texto_base_conhecimento = self.extrair_texto_base_conhecimento(base_conhecimento)
            texto_extraido = f'Arquivo: {os.path.basename(base_conhecimento.arquivo.name)} texto extraído do arquivo: {texto_base_conhecimento.replace('\n', '')}'     
            self.alimenta_contexto(arr_mensagens, "system", texto_extraido)
                 
        # Alimenta base com pergunta do usuario
        self.alimenta_pergunta_do_usuario(instancia_agente, **data)
        
        # Ultima instrucao
        ultima_instrucao = self.obter_ultima_instrucao(instancia_agente)
        if ultima_instrucao:
            self.alimenta_contexto(arr_mensagens, "system", ultima_instrucao)
            
        # Monta contexto 
        self.montar_contexto_para_envio(arr_mensagens, data_id_agente, idmaster)
            
        # Send
        response = self.enviar_para_openai("gpt-4o-mini", arr_mensagens)
        
        self.alimenta_resposta_do_gpt(response, instancia_agente, **data)    

        #Pular primeira linha, para nao enviar a instrucao do agente
        return Response(arr_mensagens[1:])
    
    
    def obter_base_conhecimento_agente(self, id_agente):
        return baseConhecimento.objects.filter(id_agente = id_agente).first()
    
    
    def extrair_texto_base_conhecimento(self, base_conhecimento):
        path = f'{MEDIA_ROOT}/{base_conhecimento.arquivo}'
            
        doc = Document(path)
        texto_extraido = '\n'.join([para.text for para in doc.paragraphs])
        
        return texto_extraido
    

    def alimenta_contexto(self, arr_mensagens, role, content):
        arr_mensagens.append({
            "role": role, 
            "content": content               
        })
        
        return arr_mensagens
    
    
    def alimenta_pergunta_do_usuario(self, instancia_agente, **data):
        Chat.objects.create(id_agente=instancia_agente, **data)
        
        
    def alimenta_resposta_do_gpt(self, response, instancia_agente, **data):
        # Criar historico do chat
        data['autor'] = 1
        data['mensagem'] = response.choices[0].message.content        
        Chat.objects.create(id_agente=instancia_agente, **data)
        
        
    def obter_ultima_instrucao(self, instancia_agente):
        ultima_instrucao = Instrucao.objects.filter(
            id_agente = instancia_agente
        ).order_by('-created_at').values('instrucao')[:1]
        
        return ultima_instrucao[0]['instrucao']
    
    
    def montar_contexto_para_envio(self, arr_mensagens, id_agente, idmaster):       
        dados = Chat.objects.filter(id_usuario = 1, id_agente = id_agente, idmaster = idmaster)
        
        for dado_chat in dados:      
            arr_mensagens.append({
                "role": dado_chat.get_autor_display(), 
                "content": dado_chat.mensagem
            })  
            
            
    def enviar_para_openai(self, model, arr_mensagens):
        """
            Envia as mensagens para a API do OpenAI e retorna a resposta.
        """
        response = openai.chat.completions.create(
            model = model,
            messages = arr_mensagens
        )
        return response