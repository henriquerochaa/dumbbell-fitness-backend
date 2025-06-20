"""
WSGI config para o projeto dumbbell.

Define a variável 'application' que os servidores web usam para rodar sua aplicação Django.

Pra saber mais, confere: 
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Define qual arquivo de configurações do Django será usado (settings.py)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dumbbell.settings')

# Cria a aplicação WSGI que o servidor vai chamar para processar requests
application = get_wsgi_application()
