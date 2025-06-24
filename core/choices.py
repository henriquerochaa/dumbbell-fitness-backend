# =============================================================================
# ARQUIVO: core/choices.py
# DESCRIÇÃO: Choices e Enums compartilhados do projeto Dumbbell Fitness
# FUNÇÃO: Define opções pré-definidas para campos de seleção nos modelos
# =============================================================================

from enum import Enum  # Enumeração para organizar choices com facilidade e clareza

"""
Choices e Enums para uso nos models Django.

Este arquivo centraliza todas as opções pré-definidas que são usadas
em campos de seleção (choices) nos modelos do projeto.

Choices disponíveis:
    - EstadoChoices: enum com todos os estados brasileiros (UFs)
    - SEXO_USUARIO: sexo do usuário (M/F/O)
    - FORMA_PAGAMENTO: formas de pagamento aceitas (Cartão/PIX/Débito)
    - BANDEIRA_CARTAO: bandeiras dos cartões (Mastercard/Visa/Elo)
    - CATEGORIA_MODALIDADES: tipos de modalidades esportivas
    - OBJETIVO_TREINO: objetivos comuns em treino (Hipertrofia/Força/etc.)
"""


class EstadoChoices(Enum):
    """
    Enum para estados brasileiros (UFs), com código e nome.
    
    Esta classe enum organiza todos os estados brasileiros de forma
    estruturada, facilitando a manutenção e uso nos modelos Django.
    
    Método choices() para usar diretamente no parâmetro choices dos fields do Django.
    """

    # Estados brasileiros organizados por região
    # Formato: SIGLA = ('SIGLA', 'Nome Completo')
    
    # Região Norte
    AC = ('AC', 'Acre')
    AP = ('AP', 'Amapá')
    AM = ('AM', 'Amazonas')
    PA = ('PA', 'Pará')
    RO = ('RO', 'Rondônia')
    RR = ('RR', 'Roraima')
    TO = ('TO', 'Tocantins')
    
    # Região Nordeste
    AL = ('AL', 'Alagoas')
    BA = ('BA', 'Bahia')
    CE = ('CE', 'Ceará')
    MA = ('MA', 'Maranhão')
    PB = ('PB', 'Paraíba')
    PE = ('PE', 'Pernambuco')
    PI = ('PI', 'Piauí')
    RN = ('RN', 'Rio Grande do Norte')
    SE = ('SE', 'Sergipe')
    
    # Região Sudeste
    ES = ('ES', 'Espírito Santo')
    MG = ('MG', 'Minas Gerais')
    RJ = ('RJ', 'Rio de Janeiro')
    SP = ('SP', 'São Paulo')
    
    # Região Sul
    PR = ('PR', 'Paraná')
    RS = ('RS', 'Rio Grande do Sul')
    SC = ('SC', 'Santa Catarina')
    
    # Região Centro-Oeste
    DF = ('DF', 'Distrito Federal')
    GO = ('GO', 'Goiás')
    MT = ('MT', 'Mato Grosso')
    MS = ('MS', 'Mato Grosso do Sul')

    @classmethod
    def choices(cls):
        """
        Retorna lista de tuplas para uso em campos Django com choices.
        
        Converte o enum em formato compatível com o Django:
        [('AC', 'Acre'), ('AL', 'Alagoas'), ...]
        
        Exemplo de uso:
            estado = models.CharField(choices=EstadoChoices.choices())
        """
        return [(member.value[0], member.value[1]) for member in cls]

    def __str__(self):
        """
        Retorna o código do estado para fácil visualização e comparação.
        
        Exemplo: EstadoChoices.SP retorna 'SP'
        """
        return self.value[0]


# =============================================================================
# CHOICES SIMPLES (LISTAS DE TUPLAS)
# =============================================================================

# Choices para Sexo do usuário
# Usado no modelo Aluno para definir o gênero
SEXO_USUARIO = [
    ('M', 'Masculino'),
    ('F', 'Feminino'),
    ('O', 'Outro'),  # Opção inclusiva para outros gêneros
]

# Choices para Forma de pagamento
# Usado no modelo Matricula para definir como o aluno vai pagar
FORMA_PAGAMENTO = [
    ('C', 'Cartão de Crédito'),  # Pagamento via cartão de crédito
    ('P', 'PIX'),                # Pagamento instantâneo via PIX
    ('D', 'Débito'),             # Pagamento via cartão de débito
]

# Choices para Bandeiras do cartão
# Usado no modelo Cartao para definir a bandeira do cartão
BANDEIRA_CARTAO = [
    ('Mastercard', 'Mastercard'),  # Cartão Mastercard
    ('Visa', 'Visa'),            # Cartão Visa
    ('Elo', 'Elo'),              # Cartão Elo (rede brasileira)
]

# Choices para Categorias das modalidades
# Usado no modelo Plano para categorizar os tipos de treino
CATEGORIA_MODALIDADES = [
    ('Musculacao', 'Musculação'),  # Treinos de força e hipertrofia
    ('Dança', 'Dança'),       # Aulas de dança
    ('Ginastica', 'Ginástica'),   # Aulas de ginástica/aeróbica
]

# Choices para Objetivos do Treino
# Usado no modelo Treino para definir o objetivo do treino
OBJETIVO_TREINO = [
    ('Hipertrofia', 'Hipertrofia'),    # Aumentar massa muscular
    ('Força', 'Força'),          # Aumentar força muscular
    ('Resistência', 'Resistência'),    # Melhorar resistência cardiovascular
    ('Emagrecimento', 'Emagrecimento'),  # Perder peso/gordura
    ('Flexibilidade', 'Flexibilidade'),  # Melhorar flexibilidade/mobilidade
]

# Choices para Disponibilidade do Treino
# Usado no modelo Treino para definir a frequência do treino
DISPONIBILIDADE_TREINO = [
    ('Diário', 'Diário'),        # Treino todos os dias
    ('Alternado', 'Alternado'),  # Treino em dias alternados
    ('Semanal', 'Semanal'),      # Treino uma vez por semana
]

GRUPO_MUSCULAR = [
    ('Biceps', 'Biceps'),
    ('Triceps', 'Triceps'),
    ('Peito', 'Peito'),
    ('Costas', 'Costas'),
    ('Ombro', 'Ombro'),
    ('Glúteos', 'Glúteos'),
    ('Panturrilha', 'Panturrilha'),
    ('Quadríceps', 'Quadríceps'),
    ('Abdominal', 'Abdominal'),
    ('Lombar', 'Lombar'),
    ('Trapézio', 'Trapézio'),
    ('Outros', 'Outros'),
]