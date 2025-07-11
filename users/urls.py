# users/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Importação para JWT Views (adicione no início do arquivo)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import (
    UserRegisterView,
    UserLoginView,
    UserProfileView,
    EstagiarioProfileViewSet,
    ResponsavelFaculdadeProfileViewSet,
    ResponsavelUPALaProfileViewSet,
    RegistroProgressoViewSet
)

# Cria um router para os ViewSets
router = DefaultRouter()
router.register(r'estagiarios_perfis', EstagiarioProfileViewSet,
                basename='estagiario-profile')
router.register(r'responsaveis_faculdade_perfis',
                ResponsavelFaculdadeProfileViewSet, basename='responsavel-faculdade-profile')
router.register(r'responsaveis_upa_perfis',
                ResponsavelUPALaProfileViewSet, basename='responsavel-upa-profile')
router.register(r'registros_progresso', RegistroProgressoViewSet,
                basename='registro-progresso')


urlpatterns = [
    # Rotas de Autenticação
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),

    # Rotas para ViewSets (perfis e registros)
    # Inclui todas as rotas registradas pelo router
    path('', include(router.urls)),

    # Rotas JWT para refresh e verify (já vêm com o simplejwt)
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

## Linha para comentários.

