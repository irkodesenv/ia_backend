from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter

router_usuario = SimpleRouter()
router_usuario.register('auth', views.AuthLogin, basename='authlogin')