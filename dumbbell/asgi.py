"""
ASGI config para o projeto dumbbell.

Define a variável 'application' que servidores ASGI usam para rodar sua aplicação Django.

Mais detalhes aqui: 
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Define qual arquivo de configurações do Django será usado
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dumbbell.settings')

# Cria a aplicação ASGI que o servidor assíncrono vai usar
application = get_asgi_application()
