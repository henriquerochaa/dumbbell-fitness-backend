#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dumbbell.settings')
django.setup()

from treinos.models import Treino
from cadastros.models import Aluno
from treinos.serializers import TreinoSerializer

def testar_nome_treino():
    print("🧪 Testando campo nome do treino...")
    
    # Buscar um aluno
    aluno = Aluno.objects.first()
    if not aluno:
        print("❌ Nenhum aluno encontrado no banco")
        return
    
    print(f"✅ Aluno encontrado: {aluno.nome} (ID: {aluno.id})")
    
    # Buscar um treino existente
    treino = Treino.objects.first()
    if not treino:
        print("❌ Nenhum treino encontrado no banco")
        return
    
    print(f"✅ Treino encontrado: ID {treino.id}")
    print(f"📝 Nome do treino no modelo: '{treino.nome}'")
    print(f"📝 Tipo do nome: {type(treino.nome)}")
    
    # Testar serializer
    try:
        serializer = TreinoSerializer(treino)
        dados_serializados = serializer.data
        print(f"📋 Dados serializados: {dados_serializados}")
        print(f"📝 Nome no serializer: '{dados_serializados.get('nome')}'")
        print(f"📝 Tipo do nome no serializer: {type(dados_serializados.get('nome'))}")
        
        if 'nome' in dados_serializados:
            print("✅ Campo 'nome' está presente no serializer")
        else:
            print("❌ Campo 'nome' NÃO está presente no serializer")
            
    except Exception as e:
        print(f"❌ Erro no serializer: {e}")
    
    # Listar todos os treinos
    print("\n📋 Listando todos os treinos:")
    treinos = Treino.objects.all()
    for t in treinos:
        print(f"  - ID: {t.id}, Nome: '{t.nome}'")

if __name__ == "__main__":
    testar_nome_treino() 