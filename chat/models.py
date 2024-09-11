from django.db import models
from agente.models import Agente


class Chat(models.Model):
    
    choice_autor = {
        ("1", "system"),
        ("2", "user")
    }
    
    idmaster = models.CharField(max_length=30)
    id_usuario = models.CharField(max_length=30)
    id_agente = models.ForeignKey(Agente, on_delete=models.CASCADE)
    autor = models.CharField(max_length=1, choices=choice_autor)
    mensagem = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    