from django.db import models
from empresa.models import Empresas
from utilitarios.views import gerarIdMaster


def agente_base_conhecimento_path(instance, filename):
    """
        Define o caminho de upload para os arquivos do agente.
        Formato: agentes/<idmaster_agente>/base_conhecimento/<filename>
    """
    return f"agentes/{instance.id_agente.idmaster}/base_conhecimento/{filename}"


def agente_logo_path(instance, filename):
    """
        Define o caminho de upload para o logo do agente.
        Formato: agente/<idmaster>/filename
    """
    return f"agente/{instance.idmaster}/{filename}"


class Agente(models.Model):
    idmaster = models.CharField(max_length=30, primary_key=True)
    nome = models.CharField(max_length=50, blank=False, null=False, default="AGENTE-IRKO")
    descritivo = models.CharField(max_length=100, blank=False, null=False, default="O que farei?")
    max_token = models.IntegerField(blank=False, null=False, default=1000)
    logo_agente = models.ImageField(upload_to=agente_logo_path, blank=True, null=True)
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


class ArquivoInstrucao(models.Model):
    id_agente = models.ForeignKey(Agente, related_name='arquivos', on_delete=models.CASCADE)
    arquivo = models.FileField(upload_to=agente_base_conhecimento_path, blank=True, null=True)


class PermissaoAgenteEmpresa(models.Model):
    id_agente = models.ForeignKey(Agente, on_delete=models.CASCADE)
    id_empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE)