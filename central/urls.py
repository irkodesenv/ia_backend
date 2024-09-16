from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from agente.urls import router_agente
from chat.urls import router_chat
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/agente/', include(router_agente.urls)),
    path('api/v1/chat/', include(router_chat.urls))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]