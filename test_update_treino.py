#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dumbbell.settings')
django.setup()

from treinos.models import Treino
from cadastros.models import Aluno
from treinos.serializers import TreinoSerializer

def testar_update_treino():
    print("🧪 Testando atualização de treino...")
    
    # Buscar um treino existente
    treino = Treino.objects.first()
    if not treino:
        print("❌ Nenhum treino encontrado no banco")
        return
    
    print(f"✅ Treino encontrado: ID {treino.id}, Nome: '{treino.nome}'")
    
    # Dados de teste para atualização
    dados_update = {
        'nome': 'Treino Atualizado Teste',
        'objetivo': 'Hipertrofia',
        'disponibilidade': 'Diário',
        'observacao': 'Teste de atualização',
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
    
    print(f"📋 Dados de atualização: {dados_update}")
    
    try:
        # Testar serializer
        serializer = TreinoSerializer(treino, data=dados_update, partial=True)
        if serializer.is_valid():
            print("✅ Dados válidos no serializer")
            treino_atualizado = serializer.save()
            print(f"✅ Treino atualizado com ID: {treino_atualizado.id}")
            print(f"✅ Nome do treino: '{treino_atualizado.nome}'")
            
            # Verificar se foi salvo no banco
            treino_db = Treino.objects.get(id=treino_atualizado.id)
            print(f"✅ Nome no banco: '{treino_db.nome}'")
            
            # Serializar novamente para ver a resposta
            dados_serializados = TreinoSerializer(treino_atualizado).data
            print(f"📋 Dados serializados: {dados_serializados}")
            print(f"📝 Nome na resposta: '{dados_serializados.get('nome')}'")
            
        else:
            print("❌ Dados inválidos no serializer")
            print(f"❌ Erros: {serializer.errors}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    testar_update_treino() 