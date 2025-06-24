#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dumbbell.settings')
django.setup()

from treinos.models import Treino
from cadastros.models import Aluno

def testar_criacao_treino():
    print("🧪 Testando criação de treino...")
    
    # Buscar um aluno
    aluno = Aluno.objects.first()
    if not aluno:
        print("❌ Nenhum aluno encontrado no banco")
        return
    
    print(f"✅ Aluno encontrado: {aluno.nome} (ID: {aluno.id})")
    
    # Criar um treino
    try:
        treino = Treino.objects.create(
            nome="Teste Nome Personalizado",
            aluno=aluno,
            objetivo="Hipertrofia",
            disponibilidade="D"
        )
        print(f"✅ Treino criado com sucesso!")
        print(f"📝 ID: {treino.id}")
        print(f"📝 Nome: {treino.nome}")
        print(f"📝 Aluno: {treino.aluno.nome}")
        print(f"📝 Objetivo: {treino.objetivo}")
        print(f"📝 Disponibilidade: {treino.disponibilidade}")
        
        # Verificar se o nome foi salvo corretamente
        treino_refresh = Treino.objects.get(id=treino.id)
        print(f"🔄 Nome após refresh: {treino_refresh.nome}")
        
        # Limpar o teste
        treino.delete()
        print("🧹 Teste limpo")
        
    except Exception as e:
        print(f"❌ Erro ao criar treino: {e}")
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    testar_criacao_treino() 