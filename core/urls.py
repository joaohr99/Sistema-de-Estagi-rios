# core/urls.py

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView  # Importe estes

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),

    # Rotas para a documentação da API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI: Swagger UI (para desenvolvimento interativo)
    path('api/schema/swagger-ui/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # Optional UI: ReDoc UI (para documentação mais formal)
    path('api/schema/redoc/',
         SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
