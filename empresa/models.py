from django.db import models


class Empresas(models.Model):
    cnpj = models.CharField(max_length=14, primary_key=True)
    razao_social = models.TextField()
    
