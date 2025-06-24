#!/usr/bin/env python3
"""
Script de teste para verificar o delete de planos.
"""

import os
import sys
import django
import requests
import json

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dumbbell.settings')
django.setup()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from planos.models import Plano
from cadastros.models import Aluno, Matricula

# Configurações da API
BASE_URL = 'http://localhost:8000'
API_BASE = f'{BASE_URL}/api/v1'

def create_test_user():
    """Cria um usuário de teste e retorna o token."""
    try:
        # Criar usuário
        user = User.objects.create_user(
            username='teste_plano_delete',
            email='teste_plano_delete@teste.com',
            password='teste123',
            first_name='Teste',
            last_name='Plano Delete'
        )
        
        # Criar token
        token, created = Token.objects.get_or_create(user=user)
        
        print(f"Usuário de teste criado: {user.username}")
        print(f"Token: {token.key}")
        
        return token.key
        
    except Exception as e:
        print(f"Erro ao criar usuário de teste: {e}")
        return None

def get_planos(token):
    """Lista todos os planos."""
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(f'{API_BASE}/planos/', headers=headers)
        print(f"Status da listagem de planos: {response.status_code}")
        
        if response.status_code == 200:
            planos = response.json()
            print(f"Planos encontrados: {len(planos)}")
            for plano in planos:
                print(f"  - ID: {plano['id']}, Título: {plano['titulo']}")
            return planos
        else:
            print(f"Erro na listagem: {response.text}")
            return []
            
    except Exception as e:
        print(f"Erro ao listar planos: {e}")
        return []

def delete_plano(token, plano_id):
    """Deleta um plano específico."""
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.delete(f'{API_BASE}/planos/{plano_id}/', headers=headers)
        print(f"Status do delete do plano {plano_id}: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Plano deletado com sucesso!")
            print(f"Mensagem: {result.get('message', 'N/A')}")
            print(f"Matrículas removidas: {result.get('matriculas_removidas', 0)}")
            print(f"Modalidades removidas: {result.get('modalidades_removidas', 0)}")
            return True
        else:
            print(f"Erro no delete: {response.text}")
            return False
            
    except Exception as e:
        print(f"Erro ao deletar plano: {e}")
        return False

def create_test_matricula(plano_id):
    """Cria uma matrícula de teste para o plano."""
    try:
        # Criar usuário para o aluno
        user = User.objects.create_user(
            username=f'teste_aluno_{plano_id}',
            email=f'teste_aluno_{plano_id}@teste.com',
            password='teste123',
            first_name='Aluno',
            last_name='Teste'
        )
        
        # Criar endereço (com campos corretos)
        from core.models import EnderecoModel
        endereco = EnderecoModel.objects.create(
            cep='12345-678',
            rua='Rua Teste',
            numero='123',
            bairro='Bairro Teste',
            cidade='Cidade Teste',
            estado='SP'
        )
        
        # Criar aluno
        aluno = Aluno.objects.create(
            user=user,
            nome='Aluno Teste',
            cpf=f'1234567890{plano_id}',
            email=f'teste_aluno_{plano_id}@teste.com',
            sexo='M',
            data_nascimento='1990-01-01',
            endereco=endereco,
            peso=70.0,
            altura=1.75
        )
        
        # Criar matrícula
        plano = Plano.objects.get(id=plano_id)
        matricula = Matricula.objects.create(
            aluno=aluno,
            plano=plano,
            forma_pagamento='C'
        )
        
        print(f"Matrícula criada para o plano '{plano.titulo}'")
        return matricula
        
    except Exception as e:
        print(f"Erro ao criar matrícula de teste: {e}")
        return None

def main():
    """Função principal do teste."""
    print("=== TESTE DE DELETE DE PLANOS ===")
    
    # 1. Criar usuário de teste
    token = create_test_user()
    if not token:
        print("Falha ao criar usuário de teste. Abortando.")
        return
    
    # 2. Listar planos existentes
    print("\n1. Listando planos existentes...")
    planos = get_planos(token)
    
    if not planos:
        print("Nenhum plano encontrado. Criando um plano de teste...")
        # Criar um plano de teste
        plano_teste = Plano.objects.create(
            titulo='Plano Teste Delete',
            preco=99.99,
            descricao='Plano para teste de delete',
            beneficios=['Teste 1', 'Teste 2']
        )
        print(f"Plano de teste criado: ID {plano_teste.id}")
        planos = get_planos(token)
    
    if not planos:
        print("Não foi possível obter planos. Abortando.")
        return
    
    # 3. Escolher um plano para deletar
    plano_para_deletar = planos[0]  # Primeiro plano da lista
    plano_id = plano_para_deletar['id']
    
    print(f"\n2. Plano selecionado para delete:")
    print(f"   ID: {plano_id}")
    print(f"   Título: {plano_para_deletar['titulo']}")
    
    # 4. Criar matrícula de teste (para testar o delete com relacionamentos)
    print(f"\n3. Criando matrícula de teste...")
    matricula = create_test_matricula(plano_id)
    
    # 5. Tentar deletar o plano
    print(f"\n4. Tentando deletar o plano...")
    success = delete_plano(token, plano_id)
    
    if success:
        print("\n✅ TESTE PASSOU: Plano deletado com sucesso!")
    else:
        print("\n❌ TESTE FALHOU: Não foi possível deletar o plano")
    
    # 6. Verificar se o plano foi realmente deletado
    print(f"\n5. Verificando se o plano foi deletado...")
    planos_apos_delete = get_planos(token)
    
    plano_ainda_existe = any(p['id'] == plano_id for p in planos_apos_delete)
    
    if not plano_ainda_existe:
        print("✅ Plano não aparece mais na listagem - DELETE FUNCIONOU!")
    else:
        print("❌ Plano ainda aparece na listagem - DELETE FALHOU!")
    
    print("\n=== FIM DO TESTE ===")

if __name__ == '__main__':
    main() 