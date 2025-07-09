from django.shortcuts import render
# users/views.py

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from rest_framework.decorators import action

from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    CustomUserSerializer,
    EstagiarioProfileSerializer,
    ResponsavelFaculdadeProfileSerializer,
    ResponsavelUPALaProfileSerializer,
    RegistroProgressoSerializer
)
from .models import (
    CustomUser,
    EstagiarioProfile,
    ResponsavelFaculdadeProfile,
    ResponsavelUPALaProfile,
    RegistroProgresso
)

# --- Views de Autenticação ---

class UserRegisterView(generics.CreateAPIView):
    """
    Endpoint para registro de novos usuários.
    Qualquer um pode se registrar.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,) # Permite que qualquer um se registre

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Opcional: Criar perfil padrão baseado no user_type
        if user.user_type == 'estagiario':
            EstagiarioProfile.objects.create(user=user)
        elif user.user_type == 'resp_faculdade':
            ResponsavelFaculdadeProfile.objects.create(user=user)
        elif user.user_type == 'resp_upa':
            ResponsavelUPALaProfile.objects.create(user=user)

        return Response({
            "message": "Usuário registrado com sucesso.",
            "user": CustomUserSerializer(user, context=self.get_serializer_context()).data
        }, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
    """
    Endpoint para login de usuários. Retorna tokens JWT.
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = CustomUser.objects.filter(username=username).first()

        if user is None or not user.check_password(password):
            return Response({'detail': 'Nome de usuário ou senha inválidos.'}, status=status.HTTP_400_BAD_REQUEST)

        # Gerar tokens JWT
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': CustomUserSerializer(user).data
        }, status=status.HTTP_200_OK)

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Endpoint para visualizar e atualizar o perfil do usuário logado.
    """
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.IsAuthenticated,) # Apenas usuários autenticados

    def get_object(self):
        return self.request.user

# --- ViewSets para Perfis Específicos e Registro de Progresso ---

class EstagiarioProfileViewSet(viewsets.ModelViewSet):
    queryset = EstagiarioProfile.objects.all()
    serializer_class = EstagiarioProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        # Um estagiário só pode ver e editar o seu próprio perfil
        if self.request.user.user_type == 'estagiario':
            return EstagiarioProfile.objects.filter(user=self.request.user)
        # Responsáveis podem ver todos os perfis de estagiários
        elif self.request.user.user_type in ['resp_faculdade', 'resp_upa']:
            return EstagiarioProfile.objects.all()
        return EstagiarioProfile.objects.none() # Outros tipos não veem nada

    def perform_create(self, serializer):
        # Garante que o perfil criado seja para o usuário logado e que ele seja um estagiário
        if self.request.user.user_type == 'estagiario':
            serializer.save(user=self.request.user)
        else:
            raise serializers.ValidationError("Apenas estagiários podem criar seu próprio perfil de estagiário.")

class ResponsavelFaculdadeProfileViewSet(viewsets.ModelViewSet):
    queryset = ResponsavelFaculdadeProfile.objects.all()
    serializer_class = ResponsavelFaculdadeProfileSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        # Um responsável de faculdade só pode ver e editar o seu próprio perfil
        if self.request.user.user_type == 'resp_faculdade':
            return ResponsavelFaculdadeProfile.objects.filter(user=self.request.user)
        # Admins podem ver todos os perfis
        if self.request.user.is_staff:
            return ResponsavelFaculdadeProfile.objects.all()
        return ResponsavelFaculdadeProfile.objects.none()

    def perform_create(self, serializer):
        if self.request.user.user_type == 'resp_faculdade':
            serializer.save(user=self.request.user)
        else:
            raise serializers.ValidationError("Apenas responsáveis de faculdade podem criar seu próprio perfil.")

class ResponsavelUPALaProfileViewSet(viewsets.ModelViewSet):
    queryset = ResponsavelUPALaProfile.objects.all()
    serializer_class = ResponsavelUPALaProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        # Um responsável de UPA só pode ver e editar o seu próprio perfil
        if self.request.user.user_type == 'resp_upa':
            return ResponsavelUPALaProfile.objects.filter(user=self.request.user)
        # Admins podem ver todos os perfis
        if self.request.user.is_staff:
            return ResponsavelUPALaProfile.objects.all()
        return ResponsavelUPALaProfile.objects.none()

    def perform_create(self, serializer):
        if self.request.user.user_type == 'resp_upa':
            serializer.save(user=self.request.user)
        else:
            raise serializers.ValidationError("Apenas responsáveis de UPA podem criar seu próprio perfil.")

class RegistroProgressoViewSet(viewsets.ModelViewSet):
    queryset = RegistroProgresso.objects.all()
    serializer_class = RegistroProgressoSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'estagiario':
            # Estagiários só veem seus próprios registros
            return RegistroProgresso.objects.filter(estagiario__user=user)
        elif user.user_type == 'resp_faculdade':
            # Responsáveis da faculdade veem registros de estagiários da mesma faculdade
            try:
                resp_faculdade_profile = ResponsavelFaculdadeProfile.objects.get(user=user)
                return RegistroProgresso.objects.filter(estagiario__faculdade=resp_faculdade_profile.faculdade)
            except ResponsavelFaculdadeProfile.DoesNotExist:
                return RegistroProgresso.objects.none()
        elif user.user_type == 'resp_upa':
            # Responsáveis da UPA veem registros de estagiários da mesma UPA
            try:
                resp_upa_profile = ResponsavelUPALaProfile.objects.get(user=user)
                return RegistroProgresso.objects.filter(estagiario__unidade_upa=resp_upa_profile.unidade_upa)
            except ResponsavelUPALaProfile.DoesNotExist:
                return RegistroProgresso.objects.none()
        return RegistroProgresso.objects.none()

    def perform_create(self, serializer):
        # Garante que o registro de progresso seja criado pelo próprio estagiário
        if self.request.user.user_type == 'estagiario':
            estagiario_profile = EstagiarioProfile.objects.get(user=self.request.user)
            serializer.save(estagiario=estagiario_profile)
        else:
            raise serializers.ValidationError("Apenas estagiários podem criar registros de progresso.")

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def update_status(self, request, pk=None):
        """
        Permite que responsáveis atualizem o status e adicionem observações.
        """
        registro = self.get_object() # Obtém o registro de progresso
        user = request.user

        # Apenas responsáveis podem alterar status e observações
        if user.user_type not in ['resp_faculdade', 'resp_upa', 'admin']:
            return Response({'detail': 'Você não tem permissão para atualizar este registro.'},
                            status=status.HTTP_403_FORBIDDEN)

        # Verificar se o responsável tem permissão para alterar este registro específico
        if user.user_type == 'resp_faculdade':
            try:
                resp_profile = ResponsavelFaculdadeProfile.objects.get(user=user)
                if registro.estagiario.faculdade != resp_profile.faculdade:
                    return Response({'detail': 'Você não tem permissão para atualizar o registro de um estagiário de outra faculdade.'},
                                    status=status.HTTP_403_FORBIDDEN)
            except ResponsavelFaculdadeProfile.DoesNotExist:
                return Response({'detail': 'Perfil de responsável da faculdade não encontrado.'}, status=status.HTTP_400_BAD_REQUEST)

        if user.user_type == 'resp_upa':
            try:
                resp_profile = ResponsavelUPALaProfile.objects.get(user=user)
                if registro.estagiario.unidade_upa != resp_profile.unidade_upa:
                    return Response({'detail': 'Você não tem permissão para atualizar o registro de um estagiário de outra UPA.'},
                                    status=status.HTTP_403_FORBIDDEN)
            except ResponsavelUPALaProfile.DoesNotExist:
                return Response({'detail': 'Perfil de responsável da UPA não encontrado.'}, status=status.HTTP_400_BAD_REQUEST)


        # Campos permitidos para atualização por responsáveis
        status_novo = request.data.get('status')
        observacoes = request.data.get('observacoes_supervisor')

        if status_novo:
            if status_novo not in [choice[0] for choice in RegistroProgresso.STATUS_CHOICES]: # Assumindo que você adicione STATUS_CHOICES no modelo RegistroProgresso
                return Response({'detail': 'Status inválido.'}, status=status.HTTP_400_BAD_REQUEST)
            registro.status = status_novo

        if observacoes is not None: # Permite definir como vazio
            registro.observacoes_supervisor = observacoes

        registro.save()
        return Response(RegistroProgressoSerializer(registro).data, status=status.HTTP_200_OK)