# Imports do Django para definição de modelos e campos
from django.db import models

# Import de validadores customizados do core
from .validators import cep_validator

# Import das choices do core
from .choices import EstadoChoices


class BaseModel(models.Model):
    """
    Modelo abstrato base para herdar campos comuns e controle básico.

    Campos:
        - criacao: Data e hora da criação do registro (auto).
        - atualizacao: Data e hora da última modificação (auto).
        - ativo: Flag para ativar/desativar registro (default True).
    """
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        abstract = True  # Não cria tabela no banco, apenas para herança


class EnderecoModel(BaseModel):
    """
    Modelo para representar endereço completo.

    Campos:
        - cep: Código postal com validação (ex: 12345-678).
        - rua: Nome da rua.
        - numero: Número da residência/estabelecimento.
        - complemento: Informação adicional (opcional).
        - bairro: Bairro do endereço.
        - cidade: Cidade do endereço.
        - estado: Estado com escolhas pré-definidas.
    """
    cep = models.CharField(
        max_length=10,
        # Validação customizada para formato de CEP
        validators=[cep_validator],
    )
    rua = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=255, blank=True, null=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(
        max_length=2,
        # Use diretamente a lista de choices, sem chamar .choices()
        choices=EstadoChoices.choices(),
    )

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'
        ordering = ['-criacao']  # Ordena do mais novo para o mais antigo

    def __str__(self):
        """
        Representação em string do endereço para facilitar visualização.
        """
        return f"{self.rua}, {self.numero} - {self.bairro} - {self.cidade}/{self.estado}"
