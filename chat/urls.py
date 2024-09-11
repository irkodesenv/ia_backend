from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter

router_chat = SimpleRouter()
router_chat.register('', views.ChatViewSet)