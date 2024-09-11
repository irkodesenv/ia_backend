from django.db import models
from empresa.models import Empresas
from utilitarios.views import gerarIdMaster


class Agente(models.Model):
    idmaster = models.CharField(max_length=30, primary_key=True)
    nome = models.CharField(max_length=50, blank=False, null=False, default="AGENTE-IRKO")
    descritivo = models.CharField(max_length=100, blank=False, null=False, default="O que farei?")
    max_token = models.IntegerField(blank=False, null=False, default=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(null = True)
    
    def save(self, *args, **kwargs):
        if not self.idmaster:
            self.idmaster = self.generate_idmaster()
        super().save(*args, **kwargs)
    
    def generate_idmaster(self):
        return gerarIdMaster()
    

class Instrucao(models.Model):
    id_agente = models.ForeignKey(Agente, related_name='instrucoes', on_delete=models.CASCADE)
    instrucao = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    

class PermissaoAgenteEmpresa(models.Model):
    id_agente = models.ForeignKey(Agente, on_delete=models.CASCADE)
    id_empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE)