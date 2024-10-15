from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from agente.urls import router_agente
from chat.urls import router_chat
from accounts.urls import router_usuario
from django.conf import settings
from django.conf.urls.static import static
from . import views
from accounts.views import CustomTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/usuario/', include(router_usuario.urls)),
    path('api/v1/agente/', include(router_agente.urls)),
    path('api/v1/chat/', include(router_chat.urls)),
    path('api/v1/get_csrf_token/', views.get_csrf_token),
    path('api/v1/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]