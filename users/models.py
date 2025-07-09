# users/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

# --- Modelos de Usuário ---


class CustomUser(AbstractUser):
    """
    Modelo de Usuário Personalizado.
    Extende o modelo de usuário padrão do Django para adicionar um campo 'user_type'.
    """
    USER_TYPE_CHOICES = (
        ('estagiario', 'Estagiário'),
        ('resp_faculdade', 'Responsável da Faculdade'),
        ('resp_upa', 'Responsável da UPA'),
    )
    user_type = models.CharField(
        max_length=20, choices=USER_TYPE_CHOICES, default='estagiario')

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.username


class EstagiarioProfile(models.Model):
    """
    Perfil específico para Estagiários.
    Relacionado um-para-um com o CustomUser.
    """
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, primary_key=True)
    faculdade = models.CharField(max_length=100)
    curso = models.CharField(max_length=100)
    # Pode ser nulo se ainda não estiver atribuído
    unidade_upa = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Perfil de Estagiário"
        verbose_name_plural = "Perfis de Estagiários"

    def __str__(self):
        return f"Perfil de {self.user.username} ({self.faculdade})"


class ResponsavelFaculdadeProfile(models.Model):
    """
    Perfil específico para Responsáveis da Faculdade.
    Relacionado um-para-um com o CustomUser.
    """
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, primary_key=True)
    faculdade = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Responsável da Faculdade"
        verbose_name_plural = "Responsáveis da Faculdade"

    def __str__(self):
        return f"Responsável: {self.user.username} ({self.faculdade})"


# Renomeei para evitar conflito com 'UPA' genérico
class ResponsavelUPALaProfile(models.Model):
    """
    Perfil específico para Responsáveis da Unidade de Pronto Atendimento (UPA).
    Relacionado um-para-um com o CustomUser.
    """
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, primary_key=True)
    unidade_upa = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Responsável da UPA"
        verbose_name_plural = "Responsáveis da UPA"

    def __str__(self):
        return f"Responsável: {self.user.username} ({self.unidade_upa})"

# --- Modelo de Registro de Progresso (Rascunho Inicial) ---


class RegistroProgresso(models.Model):
    """
    Modelo para registrar o progresso de um estagiário.
    """
    estagiario = models.ForeignKey(
        EstagiarioProfile, on_delete=models.CASCADE, related_name='registros_progresso')
    data_registro = models.DateField(auto_now_add=True)
    descricao_atividades = models.TextField()
    aprendizados = models.TextField(blank=True, null=True)
    desafios = models.TextField(blank=True, null=True)
    auto_avaliacao = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],  # Escala de 1 a 5
        help_text="Autoavaliação do desempenho (1=Ruim, 5=Excelente)"
    )
    # Campo para o responsável adicionar feedback
    observacoes_supervisor = models.TextField(blank=True, null=True)
    STATUS_CHOICES = (
        ('pendente', 'Pendente de Revisão'),
        ('revisado', 'Revisado'),
        ('aprovado', 'Aprovado'),
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,  # Usa a constante definida acima
        default='pendente'
    )

    class Meta:
        verbose_name = "Registro de Progresso"
        verbose_name_plural = "Registros de Progresso"
        # Ordena os registros do mais novo para o mais antigo
        ordering = ['-data_registro']

    def __str__(self):
        return f"Progresso de {self.estagiario.user.username} em {self.data_registro}"
