# core/urls.py

from django.contrib import admin
from django.urls import path, include # Adicione include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')), #Todas as suas URLs da API começarão com /api/
]