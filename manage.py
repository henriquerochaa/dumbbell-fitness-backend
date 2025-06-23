# =============================================================================
# ARQUIVO: manage.py
# DESCRIÇÃO: Script de gerenciamento do Django para o projeto Dumbbell Fitness
# FUNÇÃO: Ponto de entrada para comandos administrativos do Django
# =============================================================================

#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.

Este arquivo é o ponto de entrada principal para executar comandos
administrativos do Django. Ele configura o ambiente e executa os
comandos solicitados.

Comandos comuns:
- python manage.py runserver - Inicia o servidor de desenvolvimento
- python manage.py migrate - Executa migrações do banco de dados
- python manage.py createsuperuser - Cria um superusuário
- python manage.py collectstatic - Coleta arquivos estáticos
- python manage.py shell - Abre o shell interativo do Django
"""

import os
import sys


def main():
    """
    Função principal que executa tarefas administrativas.
    
    Esta função é chamada quando o script manage.py é executado.
    Ela configura o ambiente Django e executa o comando solicitado.
    
    Processo:
    1. Define o módulo de configurações do Django
    2. Importa o sistema de execução de comandos do Django
    3. Executa o comando passado como argumento
    
    Exemplo de uso:
        python manage.py runserver
        python manage.py migrate
        python manage.py createsuperuser
    """
    # Define o módulo de configurações do Django
    # Isso diz ao Django qual arquivo settings.py usar
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dumbbell.settings')
    
    try:
        # Importa o sistema de execução de comandos do Django
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Se não conseguir importar o Django, mostra erro explicativo
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Executa o comando passado como argumento
    # sys.argv contém os argumentos da linha de comando
    execute_from_command_line(sys.argv)


# Executa a função main() apenas se o script for executado diretamente
# Isso permite que o arquivo seja importado sem executar comandos
if __name__ == '__main__':
    main()
