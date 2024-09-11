from . import views
from rest_framework.routers import SimpleRouter

router_agente = SimpleRouter()
router_agente.register('', views.AgenteViewSet)
router_agente.register('instrucoes', views.InstrucaoViewSet)
