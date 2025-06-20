# Expressões regulares para validar padrões de texto (ex: CPF, CEP, datas)
import re
# Classe de exceção do Django para levantar erros de validação nos campos
from django.core.exceptions import ValidationError
# Biblioteca para manipular datas e horas, útil para validar validade de cartão, etc.
from datetime import datetime


def cep_validator(value):
    """
    Validador para CEP brasileiro.
    Espera o formato exato: 99999-999 (5 dígitos, hífen, 3 dígitos).

    Args:
        value (str): Valor do CEP a ser validado.

    Raises:
        ValidationError: Se o formato do CEP for inválido.
    """
    if not re.match(r'^\d{5}-\d{3}$', value):
        raise ValidationError('CEP deve estar no formato 99999-999')


def cpf_validator(value):
    """
    Validador para CPF brasileiro.
    Espera o formato exato: 999.999.999-99 (com pontos e hífen).

    Args:
        value (str): Valor do CPF a ser validado.

    Raises:
        ValidationError: Se o formato do CPF for inválido.
    """
    if not re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', value):
        raise ValidationError('CPF deve estar no formato 999.999.999-99')


def cnpj_validator(value):
    """
    Validador para CNPJ brasileiro.
    Espera o formato exato: 99.999.999/9999-99 (com pontos, barra e hífen).

    Args:
        value (str): Valor do CNPJ a ser validado.

    Raises:
        ValidationError: Se o formato do CNPJ for inválido.
    """
    if not re.match(r'^\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}$', value):
        raise ValidationError('CNPJ deve estar no formato 99.999.999/9999-99')


def telefone_validator(value):
    """
    Validador para números de telefone.
    Aceita números com 9 a 15 dígitos, opcionalmente iniciando com '+'.

    Args:
        value (str): Número de telefone a ser validado.

    Raises:
        ValidationError: Se o número não atender ao padrão.
    """
    if not re.match(r'^\+?\d{9,15}$', value):
        raise ValidationError(
            'Telefone deve conter entre 9 e 15 dígitos, podendo começar com +')


def validate_numero_cartao(value):
    """
    Valida que o número do cartão tem 16 dígitos numéricos.
    """
    if not value.isdigit() or len(value) != 16:
        raise ValidationError("Número do cartão deve ter 16 dígitos.")


def validate_cvv(value):
    """
    Valida que o CVV tem 3 dígitos numéricos.
    """
    if not value.isdigit() or len(value) != 3:
        raise ValidationError("CVV deve ter 3 dígitos.")


def validate_data_validade(value):
    """
    Valida o formato AAAA/MM e que o cartão não está expirado.
    """
    if not re.match(r'^\d{4}/(0[1-9]|1[0-2])$', value):
        raise ValidationError("Formato inválido. Use AAAA/MM.")

    ano, mes = map(int, value.split('/'))
    validade = datetime(ano, mes, 1)
    hoje = datetime.today().replace(day=1)

    if validade < hoje:
        raise ValidationError("Cartão expirado.")


def validate_forma_pagamento_cartao(data):
    """
    Valida a relação entre forma_pagamento e cartao.

    - Se forma_pagamento for crédito ou débito, o cartão é obrigatório.
    - Se for PIX, não pode ter cartão.
    """
    forma_pagamento = data.get('forma_pagamento')
    cartao = data.get('cartao')

    if forma_pagamento in ['C', 'D']:  # Usando siglas do seu FORMA_PAGAMENTO
        if not cartao:
            raise ValidationError({
                'cartao': 'Você precisa fornecer os dados do cartão para essa forma de pagamento.'
            })
    elif forma_pagamento == 'P':
        if cartao:
            raise ValidationError({
                'cartao': 'Não forneça dados do cartão para pagamento via PIX.'
            })


def validate_aluno_matricula_unica(data, instance=None):
    """
    Valida que o aluno não tenha matrícula ativa duplicada.

    - Ignora a própria instância caso seja update.

    Importa o modelo Matricula para fazer validações específicas relacionadas a ele
    """
    from cadastros.models import Matricula
    aluno = data.get('aluno')
    if aluno:
        qs = Matricula.objects.filter(aluno=aluno)
        if instance:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise ValidationError(
                "Aluno já possui matrícula ativa no sistema.")
