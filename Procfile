# =============================================================================
# ARQUIVO: Procfile
# DESCRIÇÃO: Configuração de deploy para plataformas como Heroku
# FUNÇÃO: Define como a aplicação deve ser executada em produção
# =============================================================================

# Comando para iniciar o servidor web em produção
# web: define um processo web (HTTP)
# gunicorn: servidor WSGI para Python
# dumbbell.wsgi: módulo WSGI da aplicação Django
# --log-file -: redireciona logs para stdout (padrão para containers)
web: gunicorn dumbbell.wsgi --log-file -
