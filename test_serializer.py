#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dumbbell.settings')
django.setup()

from treinos.serializers import TreinoSerializer
from cadastros.models import Aluno

def testar_serializer():
    print("🧪 Testando serializer de treino...")
    
    # Buscar um aluno
    aluno = Aluno.objects.first()
    if not aluno:
        print("❌ Nenhum aluno encontrado no banco")
        return
    
    print(f"✅ Aluno encontrado: {aluno.nome} (ID: {aluno.id})")
    
    # Dados de teste
    dados_teste = {
        'nome': 'Treino Teste via Serializer',
        'aluno': aluno.id,
        'objetivo': 'Hipertrofia',
        'disponibilidade': 'Diário',
        'observacao': 'Teste do serializer',
        'exercicios': [
            {
                'exercicio': 1,
                'series': 3,
                'repeticoes': 12,
                'carga': None,
                'descanso': 90
            }
        ]
    }
    
    print(f"📋 Dados de teste: {dados_teste}")
    
    try:
        # Criar serializer
        serializer = TreinoSerializer(data=dados_teste)
        
        # Validar dados
        if serializer.is_valid():
            print("✅ Dados válidos no serializer")
            
            # Criar o treino
            treino = serializer.save()
            print(f"✅ Treino criado via serializer!")
            print(f"📝 ID: {treino.id}")
            print(f"📝 Nome: {treino.nome}")
            print(f"📝 Aluno: {treino.aluno.nome}")
            print(f"📝 Objetivo: {treino.objetivo}")
            print(f"📝 Disponibilidade: {treino.disponibilidade}")
            print(f"📝 Exercícios: {treino.exercicios.count()}")
            
            # Limpar o teste
            treino.delete()
            print("🧹 Teste limpo")
            
        else:
            print("❌ Dados inválidos no serializer")
            print(f"❌ Erros: {serializer.errors}")
            
    except Exception as e:
        print(f"❌ Erro no serializer: {e}")
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    testar_serializer() 