from django.contrib import admin
from .models import Agente, Instrucao, PermissaoAgenteEmpresa, baseConhecimento


@admin.register(Agente)
class AgentesAdmin(admin.ModelAdmin):
    list_display = ('idmaster', 'nome', 'descritivo', 'max_token', 'created_at', 'update_at')
    

@admin.register(Instrucao)
class InstrucaoAdmin(admin.ModelAdmin):
    list_display = ('id_agente', 'instrucao', 'created_at')
 

@admin.register(PermissaoAgenteEmpresa)
class PermissaoAgenteEmpresaAdmin(admin.ModelAdmin):
    list_display = ('id_agente', 'id_empresa')
    
    
@admin.register(baseConhecimento)
class baseConhecimentoAdmin(admin.ModelAdmin):
    list_display = ('id_agente', 'arquivo')