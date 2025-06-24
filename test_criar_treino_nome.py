#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dumbbell.settings')
django.setup()

from treinos.models import Treino
from cadastros.models import Aluno
from treinos.serializers import TreinoSerializer

def testar_criar_treino_com_nome():
    print("🧪 Testando criação de treino com nome personalizado...")
    
    # Buscar um aluno
    aluno = Aluno.objects.first()
    if not aluno:
        print("❌ Nenhum aluno encontrado no banco")
        return
    
    print(f"✅ Aluno encontrado: {aluno.nome} (ID: {aluno.id})")
    
    # Dados de teste com nome personalizado
    dados_teste = {
        'nome': 'Treino Personalizado Teste',
        'aluno': aluno.id,
        'objetivo': 'Hipertrofia',
        'disponibilidade': 'Diário',
        'observacao': 'Teste de criação com nome personalizado',
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
        # Testar serializer
        serializer = TreinoSerializer(data=dados_teste)
        if serializer.is_valid():
            print("✅ Dados válidos no serializer")
            treino = serializer.save()
            print(f"✅ Treino criado com ID: {treino.id}")
            print(f"✅ Nome do treino: '{treino.nome}'")
            
            # Verificar se foi salvo no banco
            treino_db = Treino.objects.get(id=treino.id)
            print(f"✅ Nome no banco: '{treino_db.nome}'")
            
            # Serializar novamente para ver a resposta
            dados_serializados = TreinoSerializer(treino).data
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
    testar_criar_treino_com_nome() 