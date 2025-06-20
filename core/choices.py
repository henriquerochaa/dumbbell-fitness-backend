from enum import Enum  # Enumeração para organizar choices com facilidade e clareza

"""
Choices e Enums para uso nos models Django.

Choices disponíveis:
    - EstadoChoices: enum com todos os estados brasileiros (UFs)
    - SEXO_USUARIO: sexo do usuário
    - FORMA_PAGAMENTO: formas de pagamento aceitas
    - BANDEIRA_CARTAO: bandeiras dos cartões
    - CATEGORIA_MODALIDADES: tipos de modalidades esportivas
    - OBJETIVO_TREINO: objetivos comuns em treino
"""


class EstadoChoices(Enum):
    """
    Enum para estados brasileiros (UFs), com código e nome.

    Método choices() para usar diretamente no parâmetro choices dos fields do Django.
    """

    AC = ('AC', 'Acre')
    AL = ('AL', 'Alagoas')
    AP = ('AP', 'Amapá')
    AM = ('AM', 'Amazonas')
    BA = ('BA', 'Bahia')
    CE = ('CE', 'Ceará')
    DF = ('DF', 'Distrito Federal')
    ES = ('ES', 'Espírito Santo')
    GO = ('GO', 'Goiás')
    MA = ('MA', 'Maranhão')
    MT = ('MT', 'Mato Grosso')
    MS = ('MS', 'Mato Grosso do Sul')
    MG = ('MG', 'Minas Gerais')
    PA = ('PA', 'Pará')
    PB = ('PB', 'Paraíba')
    PR = ('PR', 'Paraná')
    PE = ('PE', 'Pernambuco')
    PI = ('PI', 'Piauí')
    RJ = ('RJ', 'Rio de Janeiro')
    RN = ('RN', 'Rio Grande do Norte')
    RS = ('RS', 'Rio Grande do Sul')
    RO = ('RO', 'Rondônia')
    RR = ('RR', 'Roraima')
    SC = ('SC', 'Santa Catarina')
    SP = ('SP', 'São Paulo')
    SE = ('SE', 'Sergipe')
    TO = ('TO', 'Tocantins')

    @classmethod
    def choices(cls):
        """
        Retorna lista de tuplas para uso em campos Django com choices.

        Exemplo:
            choices=EstadoChoices.choices()
        """
        return [(member.value[0], member.value[1]) for member in cls]

    def __str__(self):
        """
        Retorna o código do estado para fácil visualização e comparação.
        """
        return self.value[0]


# Choices para Sexo do usuário
SEXO_USUARIO = [
    ('M', 'Masculino'),
    ('F', 'Feminino'),
    ('O', 'Outro'),
]

# Choices para Forma de pagamento
FORMA_PAGAMENTO = [
    ('C', 'Cartão de Crédito'),
    ('P', 'PIX'),
    ('D', 'Débito'),
]

# Choices para Bandeiras do cartão
BANDEIRA_CARTAO = [
    ('M', 'Mastercard'),
    ('V', 'Visa'),
    ('E', 'Elo'),
]

# Choices para Categorias das modalidades
CATEGORIA_MODALIDADES = [
    ('M', 'Musculação'),
    ('D', 'Dança'),
    ('G', 'Ginástica'),
]

# Choices para Objetivos do Treino
OBJETIVO_TREINO = [
    ('H', 'Hipertrofia'),
    ('F', 'Força'),
    ('R', 'Resistência'),
    ('E', 'Emagrecimento'),
    ('X', 'Flexibilidade'),
]
