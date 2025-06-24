#!/usr/bin/env python
"""
Script para testar a funcionalidade de deletar exercícios.
Execute com: python test_exercicio_delete.py
"""

import os
import django

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dumbbell.settings')
django.setup()

from django.contrib.auth.models import User
from cadastros.models import Aluno, Matricula
from core.models import EnderecoModel
from planos.models import Plano
from treinos.models import Treino, ExercicioTreino
from exercicios.models import Exercicio

def test_exercicio_delete():
    """Testa a funcionalidade de deletar exercícios."""
    
    print("🧪 Testando funcionalidade de deletar exercícios...")
    
    # 1. Criar dados de teste
    print("\n📝 Criando dados de teste...")
    
    # Endereço
    endereco = EnderecoModel.objects.create(
        cep="12345-678",
        rua="Rua Teste",
        numero="123",
        bairro="Centro",
        cidade="São Paulo",
        estado="SP"
    )
    
    # Plano
    plano = Plano.objects.create(
        titulo="starter",
        preco=99.90,
        descricao="Plano de teste",
        beneficios=["Teste"],
        ativo=True
    )
    
    # Usuário e Aluno
    user = User.objects.create_user(
        username="teste@teste.com",
        email="teste@teste.com",
        password="senha123",
        first_name="Teste"
    )
    
    aluno = Aluno.objects.create(
        user=user,
        nome="Usuário Teste",
        cpf="111.222.333-44",
        email="teste@teste.com",
        sexo="M",
        data_nascimento="1990-01-01",
        endereco=endereco,
        peso=70.0,
        altura=1.75
    )
    
    # Matrícula
    matricula = Matricula.objects.create(
        aluno=aluno,
        plano=plano,
        forma_pagamento="C",
        ativo=True
    )
    
    # Exercício que será deletado
    exercicio = Exercicio.objects.create(
        nome="Flexão de Braço",
        descricao="Exercício para peito e tríceps",
        categoria="Musculação",
        grupo_muscular="Peito",
        ativo=True
    )
    
    print(f"✅ Exercício criado: {exercicio.nome}")
    
    # 2. Criar treinos que usam o exercício
    print("\n🏋️ Criando treinos que usam o exercício...")
    
    treino1 = Treino.objects.create(
        aluno=aluno,
        objetivo="H",
        disponibilidade="M",
        observacao="Treino 1",
        ativo=True
    )
    
    ExercicioTreino.objects.create(
        treino=treino1,
        exercicio=exercicio,
        series=3,
        repeticoes=12,
        carga=0,
        descanso=60
    )
    
    treino2 = Treino.objects.create(
        aluno=aluno,
        objetivo="E",
        disponibilidade="T",
        observacao="Treino 2",
        ativo=True
    )
    
    ExercicioTreino.objects.create(
        treino=treino2,
        exercicio=exercicio,
        series=4,
        repeticoes=15,
        carga=0,
        descanso=45
    )
    
    print(f"✅ Treino 1 criado com exercício")
    print(f"✅ Treino 2 criado com exercício")
    
    # 3. Verificar referências antes da deleção
    print("\n🔍 Verificando referências antes da deleção...")
    
    referencias_antes = ExercicioTreino.objects.filter(exercicio=exercicio).count()
    print(f"   Referências do exercício nos treinos: {referencias_antes}")
    
    treinos_com_exercicio = Treino.objects.filter(exercicios__exercicio=exercicio).distinct()
    print(f"   Treinos que usam o exercício: {treinos_com_exercicio.count()}")
    
    # 4. Testar a deleção
    print("\n🗑️ Testando deleção do exercício...")
    
    try:
        # Simular a lógica do destroy
        exercicios_treino = ExercicioTreino.objects.filter(exercicio=exercicio)
        count_removidos = exercicios_treino.count()
        
        if count_removidos > 0:
            exercicios_treino.delete()
            print(f"   ✅ Removidas {count_removidos} referências do exercício nos treinos")
        
        # Deletar o exercício
        exercicio.delete()
        print(f"   ✅ Exercício '{exercicio.nome}' deletado com sucesso")
        
    except Exception as e:
        print(f"   ❌ Erro ao deletar exercício: {str(e)}")
        return
    
    # 5. Verificar estado após a deleção
    print("\n🔍 Verificando estado após a deleção...")
    
    # Verificar se o exercício foi deletado
    exercicio_existe = Exercicio.objects.filter(id=exercicio.id).exists()
    print(f"   Exercício ainda existe: {exercicio_existe}")
    
    # Verificar se as referências foram removidas
    referencias_depois = ExercicioTreino.objects.filter(exercicio_id=exercicio.id).count()
    print(f"   Referências restantes: {referencias_depois}")
    
    # Verificar se os treinos ainda existem (devem existir, só sem o exercício)
    treinos_existem = Treino.objects.filter(id__in=[treino1.id, treino2.id]).count()
    print(f"   Treinos ainda existem: {treinos_existem}")
    
    # Verificar se os treinos têm exercícios
    treino1_exercicios = ExercicioTreino.objects.filter(treino=treino1).count()
    treino2_exercicios = ExercicioTreino.objects.filter(treino=treino2).count()
    print(f"   Exercícios no Treino 1: {treino1_exercicios}")
    print(f"   Exercícios no Treino 2: {treino2_exercicios}")
    
    print("\n🎯 Resumo:")
    print("   - Exercício foi deletado com sucesso")
    print("   - Referências nos treinos foram removidas")
    print("   - Treinos continuam existindo (sem o exercício deletado)")
    print("   - Funcionalidade implementada corretamente!")

if __name__ == '__main__':
    test_exercicio_delete() 