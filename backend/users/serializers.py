# users/serializers.py

from rest_framework import serializers
from .models import CustomUser, EstagiarioProfile, ResponsavelFaculdadeProfile, ResponsavelUPALaProfile, RegistroProgresso

# --- Serializers para Autenticação e Usuários ---

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'user_type', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}} # Garante que a senha não seja retornada na resposta

    def create(self, validated_data):
        # Cria o usuário com a senha criptografada
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            user_type=validated_data.get('user_type', 'estagiario'), # Define o tipo padrão
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer para exibir dados do usuário, excluindo a senha.
    """
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'user_type', 'first_name', 'last_name', 'is_staff')
        read_only_fields = ('user_type',) # user_type não deve ser alterado após o registro inicial

# --- Serializers para Perfis ---

class EstagiarioProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True) # Inclui os dados do usuário associado

    class Meta:
        model = EstagiarioProfile
        fields = '__all__' # Inclui todos os campos do modelo
        read_only_fields = ('user',) # O campo 'user' é preenchido automaticamente, não pelo usuário

class ResponsavelFaculdadeProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = ResponsavelFaculdadeProfile
        fields = '__all__'
        read_only_fields = ('user',)

class ResponsavelUPALaProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = ResponsavelUPALaProfile
        fields = '__all__'
        read_only_fields = ('user',)

# --- Serializers para Registro de Progresso ---

class RegistroProgressoSerializer(serializers.ModelSerializer):
    estagiario = EstagiarioProfileSerializer(read_only=True) # Mostra os dados do estagiário associado

    class Meta:
        model = RegistroProgresso
        fields = '__all__' # Todos os campos
        read_only_fields = ('estagiario', 'data_registro', 'status', 'observacoes_supervisor') # Campos que não são editáveis pelo estagiário