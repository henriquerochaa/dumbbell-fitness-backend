# Dumbbell Fitness API

API REST para gerenciar planos, alunos, exercícios e treinos de uma academia fictícia Dumbbell Fitness.

---

## Tecnologias

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

- **cadastros**: gerenciamento de alunos, matrículas e cartões
- **exercicios**: cadastro e controle dos exercícios físicos
- **planos**: planos de treino, modalidades e relacionamentos
- **treinos**: criação e controle dos treinos dos alunos
- **core**: modelos base e escolhas compartilhadas

---

## Configuração

1. Clone o repositório
2. Crie e ative seu ambiente virtual
3. Instale as dependências:
4. Rode o comando "pip install -r requirements.txt"

## Crie um arquivo .env na raiz do projeto com as variáveis:

    SECRET_KEY=sua_chave_gerada_pelo_comando_django
    DEBUG=True
    DATABASE_URL=postgres://usuario:senha@endereco:porta/banco

## Para gerar uma SECRET_KEY segura, execute:

    python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

## Rode as migrações para criar as tabelas no banco:

    python manage.py migrate

## Crie um superusuário para acessar o admin e testar:

    python manage.py createsuperuser

## Rode o servidor:

    python manage.py runserver

## Autenticação - Obter Token

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

Resposta sucesso (HTTP 200):

    {
      "token": "seu_token_de_acesso_aqui"
    }

Exemplo para obter token usando Python requests

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

Exemplo de POST para Criar um Treino

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
