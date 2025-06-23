# Dumbbell Fitness API

# <!--

ARQUIVO: README.md
DESCRIÇÃO: Documentação principal do projeto Dumbbell Fitness
FUNÇÃO: Guia completo de instalação, configuração e uso da API
=============================================================================
-->

API REST completa para gerenciamento de academia fictícia Dumbbell Fitness, desenvolvida com Django REST Framework.

<!--
ESTRUTURA DO PROJETO:
- Backend Django com Django REST Framework
- Banco de dados PostgreSQL
- Autenticação via token
- API RESTful completa
- Deploy configurado para Heroku
-->

---

## 🚀 Tecnologias

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

- **Python 3.13.3** - Linguagem principal
- **Django 5.2** - Framework web
- **Django REST Framework** - API REST
- **PostgreSQL** - Banco de dados
- **django-cors-headers** - CORS para frontend
- **dj-database-url** - Configuração de banco via URL
- **python-dotenv** - Variáveis de ambiente
- **django-filter** - Filtros avançados
- **whitenoise** - Servir arquivos estáticos

---

## 📁 Estrutura do Projeto

<!--
APPS DO PROJETO:
- cadastros: Gerenciamento de alunos, matrículas e cartões
- exercicios: Cadastro e controle dos exercícios físicos
- planos: Planos de treino, modalidades e relacionamentos
- treinos: Criação e controle dos treinos dos alunos
- core: Modelos base e escolhas compartilhadas
-->

```
dumbbell-fitness-backend/
├── cadastros/          # Gerenciamento de alunos, matrículas e cartões
├── core/              # Modelos base e escolhas compartilhadas
├── exercicios/        # Cadastro e controle dos exercícios físicos
├── planos/            # Planos de treino, modalidades e relacionamentos
├── treinos/           # Criação e controle dos treinos dos alunos
├── dumbbell/          # Configurações principais do projeto
├── manage.py          # Script de gerenciamento Django
├── requirements.txt   # Dependências do projeto
└── .env              # Variáveis de ambiente (não versionado)
```

---

## ⚙️ Configuração

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

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd dumbbell-fitness-backend
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv fit
source fit/bin/activate  # Linux/Mac
# ou
fit\Scripts\activate     # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

<!--
VARIÁVEIS DE AMBIENTE NECESSÁRIAS:
- SECRET_KEY: Chave secreta do Django (gerada automaticamente)
- DEBUG: Modo debug (True para desenvolvimento, False para produção)
- DATABASE_URL: URL de conexão com o banco PostgreSQL
-->

    SECRET_KEY=sua_chave_secreta_aqui
    DEBUG=True
    DATABASE_URL=postgres://usuario:senha@endereco:porta/banco

**Para gerar uma SECRET_KEY segura:**

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Execute as migrações

```bash
python manage.py migrate
```

### 6. Crie um superusuário

```bash
python manage.py createsuperuser
```

### 7. Inicie o servidor

```bash
python manage.py runserver
```

O servidor estará disponível em: `http://localhost:8000`

---

## 🔐 Autenticação

A API usa autenticação via token. Para acessar endpoints protegidos, obtenha um token:

### Obter Token de Autenticação

**Endpoint:** `POST /api/v1/planos/auth/login/`

**Headers:**

```
Content-Type: application/json
```

**Body:**

```json
{
  "username": "seu_usuario",
  "password": "sua_senha"
}
```

**Resposta de Sucesso (200):**

```json
{
  "token": "seu_token_de_acesso_aqui",
  "user": {
    "id": 1,
    "username": "seu_usuario",
    "email": "usuario@email.com",
    "first_name": "Nome",
    "last_name": "Sobrenome"
  }
}
```

### Usar Token nas Requisições

**Headers:**

```
Authorization: Token seu_token_aqui
Content-Type: application/json
```

---

## 📡 Endpoints da API

### 🔓 Endpoints Públicos (sem autenticação)

#### Planos

- `GET /api/v1/planos/` - Lista todos os planos ativos
- `GET /api/v1/planos/{id}/` - Detalhes de um plano específico

#### Exercícios

- `GET /api/v1/exercicios/` - Lista todos os exercícios
- `GET /api/v1/exercicios/{id}/` - Detalhes de um exercício
- `POST /api/v1/exercicios/` - Criar novo exercício
- `PUT /api/v1/exercicios/{id}/` - Atualizar exercício
- `DELETE /api/v1/exercicios/{id}/` - Deletar exercício

### 🔒 Endpoints Protegidos (requer autenticação)

#### Autenticação

- `POST /api/v1/planos/auth/login/` - Login e obter token
- `GET /api/v1/planos/auth/user/` - Informações do usuário logado

#### Treinos

- `GET /api/v1/treinos/` - Lista treinos do usuário logado
- `GET /api/v1/treinos/{id}/` - Detalhes de um treino
- `POST /api/v1/treinos/` - Criar novo treino
- `PUT /api/v1/treinos/{id}/` - Atualizar treino
- `DELETE /api/v1/treinos/{id}/` - Deletar treino

#### Cadastros (Alunos)

- `GET /api/v1/cadastros/alunos/` - Lista alunos
- `POST /api/v1/cadastros/alunos/` - Cadastrar novo aluno
- `GET /api/v1/cadastros/alunos/{id}/` - Detalhes do aluno
- `PUT /api/v1/cadastros/alunos/{id}/` - Atualizar aluno
- `DELETE /api/v1/cadastros/alunos/{id}/` - Deletar aluno

---

## 📊 Modelos de Dados

### Plano

```json
{
  "id": 1,
  "titulo": "Plano Starter",
  "preco": "99.90",
  "descricao": "Plano ideal para iniciantes",
  "beneficios": [
    "Atendimento exclusivo com professores",
    "Acesso a todas as modalidades",
    "Acesso ilimitado à unidade"
  ],
  "ativo": true
}
```

### Exercício

```json
{
  "id": 1,
  "nome": "Supino Reto",
  "descricao": "Exercício para peitoral",
  "grupo_muscular": "Peitoral",
  "equipamento": "Barra",
  "dificuldade": "Intermediário"
}
```

### Treino

```json
{
  "id": 1,
  "objetivo": "Hipertrofia",
  "disponibilidade": "3x por semana",
  "observacao": "Treino focado em força",
  "exercicios": [
    {
      "exercicio": 1,
      "series": 3,
      "repeticoes": 12,
      "carga": 50.0,
      "descanso": 90
    }
  ]
}
```

---

## 🌐 CORS

A API está configurada para permitir requisições de qualquer origem (`CORS_ALLOW_ALL_ORIGINS = True`), ideal para desenvolvimento e demonstração acadêmica.

---

## 🚀 Deploy

O projeto está configurado para deploy no Heroku com:

- `Procfile` configurado
- `whitenoise` para arquivos estáticos
- Configuração de banco via `DATABASE_URL`

---

## 📝 Exemplos de Uso

### Python (requests)

```python
import requests

# Obter token
url = "http://localhost:8000/api/v1/planos/auth/login/"
data = {"username": "admin", "password": "senha123"}
response = requests.post(url, json=data)
token = response.json()["token"]

# Listar planos (público)
planos = requests.get("http://localhost:8000/api/v1/planos/")
print(planos.json())

# Criar treino (protegido)
headers = {"Authorization": f"Token {token}"}
treino_data = {
    "objetivo": "Hipertrofia",
    "disponibilidade": "3x por semana",
    "observacao": "Treino focado em força"
}
response = requests.post("http://localhost:8000/api/v1/treinos/",
                        json=treino_data, headers=headers)
```

### JavaScript (fetch)

```javascript
// Obter token
const response = await fetch(
  "http://localhost:8000/api/v1/planos/auth/login/",
  {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username: "admin", password: "senha123" }),
  }
);
const { token } = await response.json();

// Listar exercícios (público)
const exercicios = await fetch("http://localhost:8000/api/v1/exercicios/");
const dados = await exercicios.json();

// Criar treino (protegido)
const treino = await fetch("http://localhost:8000/api/v1/treinos/", {
  method: "POST",
  headers: {
    Authorization: `Token ${token}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    objetivo: "Hipertrofia",
    disponibilidade: "3x por semana",
  }),
});
```

---

## 🔧 Comandos Úteis

```bash
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Shell do Django
python manage.py shell

# Coletar arquivos estáticos
python manage.py collectstatic

# Testes
python manage.py test
```

---

## 📚 Documentação Adicional

- **Admin Django:** `http://localhost:8000/admin/`
- **API Browsable:** `http://localhost:8000/api/v1/`
- **Autenticação:** `http://localhost:8000/auth/`

---

## 🤝 Contribuição

Este projeto foi desenvolvido para fins acadêmicos. Para contribuições:

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
