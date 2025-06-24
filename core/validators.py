# =============================================================================
# ARQUIVO: core/validators.py
# DESCRIÇÃO: Validadores customizados do projeto Dumbbell Fitness
# FUNÇÃO: Define funções de validação para campos específicos dos modelos
# =============================================================================

# Expressões regulares para validar padrões de texto (ex: CPF, CEP, datas)
import re
# Classe de exceção do Django para levantar erros de validação nos campos
from django.core.exceptions import ValidationError
# Biblioteca para manipular datas e horas, útil para validar validade de cartão, etc.
from datetime import datetime


def cep_validator(value):
    """
    Validador para CEP brasileiro.
    
    Verifica se o CEP está no formato correto: 99999-999 (5 dígitos, hífen, 3 dígitos).
    
    Args:
        value (str): Valor do CEP a ser validado.
        
    Raises:
        ValidationError: Se o formato do CEP for inválido.
        
    Exemplo:
        cep_validator("12345-678")  # Válido
        cep_validator("12345678")   # Inválido (falta hífen)
        cep_validator("1234-567")   # Inválido (formato incorreto)
    """
    if not re.match(r'^\d{5}-\d{3}$', value):
        raise ValidationError('CEP deve estar no formato 99999-999')


def cpf_validator(value):
    """
    Validador para CPF brasileiro.
    
    Verifica se o CPF está no formato correto: 999.999.999-99 (com pontos e hífen).
    
    Args:
        value (str): Valor do CPF a ser validado.
        
    Raises:
        ValidationError: Se o formato do CPF for inválido.
        
    Exemplo:
        cpf_validator("123.456.789-01")  # Válido
        cpf_validator("12345678901")     # Inválido (falta formatação)
    """
    if not re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', value):
        raise ValidationError('CPF deve estar no formato 999.999.999-99')


def cnpj_validator(value):
    """
    Validador para CNPJ brasileiro.
    
    Verifica se o CNPJ está no formato correto: 99.999.999/9999-99 (com pontos, barra e hífen).
    
    Args:
        value (str): Valor do CNPJ a ser validado.
        
    Raises:
        ValidationError: Se o formato do CNPJ for inválido.
        
    Exemplo:
        cnpj_validator("12.345.678/0001-90")  # Válido
        cnpj_validator("12345678000190")      # Inválido (falta formatação)
    """
    if not re.match(r'^\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}$', value):
        raise ValidationError('CNPJ deve estar no formato 99.999.999/9999-99')


def telefone_validator(value):
    """
    Validador para números de telefone.
    
    Aceita números com 9 a 15 dígitos, opcionalmente iniciando com '+'.
    Útil para validar telefones brasileiros e internacionais.
    
    Args:
        value (str): Número de telefone a ser validado.
        
    Raises:
        ValidationError: Se o número não atender ao padrão.
        
    Exemplo:
        telefone_validator("11999999999")     # Válido (celular brasileiro)
        telefone_validator("+5511999999999")  # Válido (com código do país)
        telefone_validator("123456")          # Inválido (muito curto)
    """
    if not re.match(r'^\+?\d{9,15}$', value):
        raise ValidationError(
            'Telefone deve conter entre 9 e 15 dígitos, podendo começar com +')


def validate_numero_cartao(value):
    """
    Valida que o número do cartão tem 16 dígitos numéricos.
    
    Verifica se o número do cartão tem o formato padrão de 16 dígitos.
    Não valida se é um número de cartão real (isso seria feito por uma API externa).
    
    Args:
        value (str): Número do cartão a ser validado.
        
    Raises:
        ValidationError: Se o número não tiver 16 dígitos.
        
    Exemplo:
        validate_numero_cartao("1234567890123456")  # Válido
        validate_numero_cartao("123456789012345")   # Inválido (15 dígitos)
        validate_numero_cartao("12345678901234567") # Inválido (17 dígitos)
    """
    if not value.isdigit() or len(value) != 16:
        raise ValidationError("Número do cartão deve ter 16 dígitos.")


def validate_cvv(value):
    """
    Valida que o CVV tem 3 dígitos numéricos.
    
    Verifica se o código de segurança do cartão tem 3 dígitos.
    
    Args:
        value (str): CVV a ser validado.
        
    Raises:
        ValidationError: Se o CVV não tiver 3 dígitos.
        
    Exemplo:
        validate_cvv("123")  # Válido
        validate_cvv("12")   # Inválido (2 dígitos)
        validate_cvv("1234") # Inválido (4 dígitos)
    """
    if not value.isdigit() or len(value) != 3:
        raise ValidationError("CVV deve ter 3 dígitos.")


def validate_data_validade(value):
    """
    Valida o formato AAAA/MM e que o cartão não está expirado.
    
    Verifica se a data de validade está no formato correto e se o cartão
    ainda não expirou.
    
    Args:
        value (str): Data de validade no formato AAAA/MM.
        
    Raises:
        ValidationError: Se o formato for inválido ou o cartão estiver expirado.
        
    Exemplo:
        validate_data_validade("2025/12")  # Válido (futuro)
        validate_data_validade("2020/01")  # Inválido (expirado)
        validate_data_validade("2025-12")  # Inválido (formato incorreto)
    """
    if not re.match(r'^\d{4}/(0[1-9]|1[0-2])$', value):
        raise ValidationError("Formato inválido. Use AAAA/MM.")

    # Extrai ano e mês da string
    ano, mes = map(int, value.split('/'))
    
    # Cria objeto datetime para a data de validade
    validade = datetime(ano, mes, 1)
    
    # Data atual (primeiro dia do mês para comparação)
    hoje = datetime.today().replace(day=1)

    # Verifica se o cartão já expirou
    if validade < hoje:
        raise ValidationError("Cartão expirado.")


def validate_forma_pagamento_cartao(data):
    """
    Valida a relação entre forma_pagamento e cartao.
    
    Regras de validação:
    - Se forma_pagamento for crédito ou débito, o cartão é obrigatório.
    - Se for PIX, não pode ter cartão.
    
    Args:
        data (dict): Dados da matrícula contendo forma_pagamento e cartao.
        
    Raises:
        ValidationError: Se a relação entre forma de pagamento e cartão for inválida.
        
    Exemplo:
        # Válido - Cartão de crédito com dados do cartão
        validate_forma_pagamento_cartao({
            'forma_pagamento': 'C',
            'cartao': 1
        })
        
        # Inválido - Cartão de crédito sem dados do cartão
        validate_forma_pagamento_cartao({
            'forma_pagamento': 'C',
            'cartao': None
        })
        
        # Inválido - PIX com dados do cartão
        validate_forma_pagamento_cartao({
            'forma_pagamento': 'P',
            'cartao': 1
        })
    """
    forma_pagamento = data.get('forma_pagamento')
    cartao = data.get('cartao')

    # Se for cartão de crédito ou débito, o cartão é obrigatório
    if forma_pagamento in ['C', 'D']:  # Usando siglas do FORMA_PAGAMENTO
        if not cartao:
            raise ValidationError({
                'cartao': 'Você precisa fornecer os dados do cartão para essa forma de pagamento.'
            })
    # Se for PIX, não pode ter cartão
    elif forma_pagamento == 'P':
        if cartao:
            raise ValidationError({
                'cartao': 'Não forneça dados do cartão para pagamento via PIX.'
            })


def validate_aluno_matricula_unica(data, instance=None):
    """
    Valida que o aluno não tenha matrícula ativa duplicada.
    
    Impede que um aluno tenha mais de uma matrícula ativa no sistema.
    Ignora a própria instância caso seja um update (edição).
    Considera apenas matrículas com campo 'ativo=True'.
    
    Args:
        data (dict): Dados da matrícula contendo o aluno.
        instance (Matricula, optional): Instância atual sendo editada.
        
    Raises:
        ValidationError: Se o aluno já possui matrícula ativa.
        
    Exemplo:
        # Inválido - Aluno já tem matrícula ativa
        validate_aluno_matricula_unica({
            'aluno': 1
        })
        
        # Válido - Primeira matrícula do aluno
        validate_aluno_matricula_unica({
            'aluno': 2
        })
    """
    # Importa o modelo Matricula para fazer validações específicas
    from cadastros.models import Matricula
    
    aluno = data.get('aluno')
    if aluno:
        # Busca apenas matrículas ativas do aluno
        qs = Matricula.objects.filter(aluno=aluno, ativo=True)
        
        # Se for um update, exclui a própria instância da busca
        if instance:
            qs = qs.exclude(pk=instance.pk)
        
        # Se encontrar alguma matrícula ativa, levanta erro
        if qs.exists():
            raise ValidationError(
                "Aluno já possui matrícula ativa no sistema.")
