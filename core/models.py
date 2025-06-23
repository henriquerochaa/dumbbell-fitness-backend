# =============================================================================
# ARQUIVO: core/models.py
# DESCRIÇÃO: Modelos base e compartilhados do projeto Dumbbell Fitness
# FUNÇÃO: Define modelos que são usados por outros apps (BaseModel, EnderecoModel)
# =============================================================================

# Imports do Django para definição de modelos e campos
from django.db import models

# Import de validadores customizados do core
from .validators import cep_validator

# Import das choices do core (estados brasileiros)
from .choices import EstadoChoices


class BaseModel(models.Model):
    """
    Modelo abstrato base para herdar campos comuns e controle básico.
    
    Este modelo fornece campos padrão que são úteis em todos os modelos:
    - criacao: Data e hora da criação do registro (auto)
    - atualizacao: Data e hora da última modificação (auto)
    - ativo: Flag para ativar/desativar registro (soft delete)
    
    Herde este modelo em outros modelos para ter esses campos automaticamente.
    """
    # Data e hora de criação do registro (preenchido automaticamente)
    criacao = models.DateTimeField(auto_now_add=True)
    
    # Data e hora da última atualização (atualizado automaticamente a cada save)
    atualizacao = models.DateTimeField(auto_now=True)
    
    # Flag para ativar/desativar registro (soft delete)
    # True = ativo, False = inativo/deletado
    ativo = models.BooleanField(default=True)

    class Meta:
        # Modelo abstrato - não cria tabela no banco, apenas para herança
        abstract = True


class EnderecoModel(BaseModel):
    """
    Modelo para representar endereço completo.
    
    Este modelo armazena informações completas de endereço que podem ser
    reutilizadas por outros modelos (Aluno, Academia, etc.).
    
    Campos obrigatórios: cep, rua, numero, bairro, cidade, estado
    Campo opcional: complemento
    """
    # CEP com validação customizada (formato: 12345-678)
    cep = models.CharField(
        max_length=10,
        validators=[cep_validator],  # Validação customizada para formato de CEP
    )
    
    # Nome da rua/avenida
    rua = models.CharField(max_length=255)
    
    # Número da residência/estabelecimento
    numero = models.CharField(max_length=10)
    
    # Informação adicional (apartamento, sala, etc.) - opcional
    complemento = models.CharField(max_length=255, blank=True, null=True)
    
    # Bairro do endereço
    bairro = models.CharField(max_length=100)
    
    # Cidade do endereço
    cidade = models.CharField(max_length=100)
    
    # Estado com escolhas pré-definidas (siglas dos estados brasileiros)
    estado = models.CharField(
        max_length=2,
        choices=EstadoChoices.choices(),  # Lista de estados brasileiros
    )

    class Meta:
        # Configurações de meta para o modelo EnderecoModel
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'
        ordering = ['-criacao']  # Ordena do mais novo para o mais antigo

    def __str__(self):
        """
        Representação em string do endereço para facilitar visualização.
        
        Retorna: "Rua Exemplo, 123 - Bairro - Cidade/SP"
        """
        return f"{self.rua}, {self.numero} - {self.bairro} - {self.cidade}/{self.estado}"
