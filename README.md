# Dumbbell Fitness API

# <!--

ARQUIVO: README.md
DESCRIÇÃO: Documentação principal do projeto Dumbbell Fitness
FUNÇÃO: Guia completo de instalação, configuração e uso da API
=============================================================================
-->

API REST para gerenciar planos, alunos, exercícios e treinos de uma academia fictícia Dumbbell Fitness.

<!--
ESTRUTURA DO PROJETO:
- Backend Django com Django REST Framework
- Banco de dados PostgreSQL
- Autenticação via token
- API RESTful completa
- Deploy configurado para Heroku
-->

---

## Tecnologias

<!--
STACK TECNOLÓGICA:
- Python 3.13.3: Linguagem principal
- Django 5.2: Framework web
- Django REST Framework: API REST
- PostgreSQL: Banco de dados
- dj-database-url: Configuração de banco via URL
- python-dotenv: Variáveis de ambiente
- django-filter: Filtros avançados
- whitenoise: Servir arquivos estáticos
-->

- Python 3.13.3
- Django 5.2
- Django REST Framework
- PostgreSQL
- dj-database-url
- python-dotenv
- django-filter
- whitenoise

---

## Estrutura do Projeto

<!--
APPS DO PROJETO:
- cadastros: Gerenciamento de alunos, matrículas e cartões
- exercicios: Cadastro e controle dos exercícios físicos
- planos: Planos de treino, modalidades e relacionamentos
- treinos: Criação e controle dos treinos dos alunos
- core: Modelos base e escolhas compartilhadas
-->

- **cadastros**: gerenciamento de alunos, matrículas e cartões
- **exercicios**: cadastro e controle dos exercícios físicos
- **planos**: planos de treino, modalidades e relacionamentos
- **treinos**: criação e controle dos treinos dos alunos
- **core**: modelos base e escolhas compartilhadas

---

## Configuração

<!--
PASSO A PASSO DE CONFIGURAÇÃO:
1. Clone o repositório
2. Crie e ative seu ambiente virtual
3. Instale as dependências
4. Configure as variáveis de ambiente
5. Execute as migrações
6. Crie um superusuário
7. Inicie o servidor
-->

1. Clone o repositório
2. Crie e ative seu ambiente virtual
3. Instale as dependências:
4. Rode o comando "pip install -r requirements.txt"

## Crie um arquivo .env na raiz do projeto com as variáveis:

<!--
VARIÁVEIS DE AMBIENTE NECESSÁRIAS:
- SECRET_KEY: Chave secreta do Django (gerada automaticamente)
- DEBUG: Modo debug (True para desenvolvimento, False para produção)
- DATABASE_URL: URL de conexão com o banco PostgreSQL
-->

    SECRET_KEY=sua_chave_gerada_pelo_comando_django
    DEBUG=True
    DATABASE_URL=postgres://usuario:senha@endereco:porta/banco

## Para gerar uma SECRET_KEY segura, execute:

<!--
GERAÇÃO DE SECRET_KEY:
Comando para gerar uma chave secreta segura para o Django
-->

    python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

## Rode as migrações para criar as tabelas no banco:

<!--
MIGRAÇÕES:
Cria todas as tabelas no banco de dados baseadas nos modelos Django
-->

    python manage.py migrate

## Crie um superusuário para acessar o admin e testar:

<!--
SUPERUSUÁRIO:
Cria um usuário administrador para acessar o painel admin do Django
-->

    python manage.py createsuperuser

## Rode o servidor:

<!--
SERVIDOR DE DESENVOLVIMENTO:
Inicia o servidor Django na porta 8000
-->

    python manage.py runserver

---

## Autenticação - Obter Token

<!--
SISTEMA DE AUTENTICAÇÃO:
A API usa autenticação via token. Para acessar endpoints protegidos,
é necessário obter um token de autenticação.
-->

    Para acessar os endpoints protegidos, obtenha um token de autenticação via:

    Requisição para obter o token

    URL: POST /api-token-auth/

    Headers:
    Content-Type: application/json

    Body JSON:

    {
    "username": "seu_usuario",
    "password": "sua_senha"
    }

### Resposta sucesso (HTTP 200):

<!--
RESPOSTA DE AUTENTICAÇÃO:
Retorna o token que deve ser usado nos headers das requisições
-->

    {
      "token": "seu_token_de_acesso_aqui"a
    }

---

## Exemplo para obter token usando Python requests

<!--
EXEMPLO PRÁTICO:
Código Python para obter token de autenticação
-->

    ```python
    import requests

    url = "http://localhost:8000/api-token-auth/"
    data = {
    "username": "seu_usuario",
    "password": "sua_senha"
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
    token = response.json().get("token")
    print("Token recebido:", token)
    else:
    print("Falha ao obter token:", response.status_code, response.text)

    ```

---

## Exemplo de POST para Criar um Treino

<!--
EXEMPLO DE USO DA API:
Demonstra como criar um treino usando a API com autenticação
-->

    ```python
    import requests

    url = "http://localhost:8000/api/v1/treinos/"

    data = {
    "objetivo": "A", # substitua conforme seu plano
    "disponibilidade": "B",
    "observacao": "Treino focado em força",
    "exercicios": [
    {
    "exercicio": 1, # ID do exercício existente
    "series": 3,
    "repeticoes": 12,
    "carga": 50.0,
    "descanso": 90
    },
    {
    "exercicio": 2,
    "series": 4,
    "repeticoes": 10,
    "carga": 40.0,
    "descanso": 60
    }
    ]
    }

    token = "seu_token_de_acesso_aqui"

    headers = {
    "Authorization": f"Token {token}",
    "Content-Type": "application/json"
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 201:
    print("Recurso criado com sucesso!")
    print("Resposta:", response.json())
    else:
    print("Erro ao criar recurso:", response.status_code, response.text)

    ```

<!--
NOTAS ADICIONAIS:
- A API está configurada para CORS, permitindo requisições do frontend
- Todos os endpoints seguem padrões RESTful
- Validações são feitas automaticamente pelos serializers
- Logs são configurados para produção
-->
