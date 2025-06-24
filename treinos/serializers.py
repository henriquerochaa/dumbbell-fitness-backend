from rest_framework import serializers
from .models import Treino, ExercicioTreino
from exercicios.models import Exercicio
from cadastros.models import Matricula
from core.choices import OBJETIVO_TREINO


class ExercicioTreinoSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo ExercicioTreino.

    Manipula os dados relacionados a cada exercício dentro de um treino.
    """
    class Meta:
        model = ExercicioTreino
        fields = (
            'exercicio',
            'series',
            'repeticoes',
            'carga',
            'descanso',
        )


class TreinoSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo Treino.

    Inclui os exercícios associados, além de validar regras de negócio,
    como limite de treinos por plano e existência de matrícula válida.
    """
    exercicios = ExercicioTreinoSerializer(many=True)

    class Meta:
        model = Treino
        fields = (
            'id',
            'nome',
            'aluno',
            'objetivo',
            'observacao',
            'peso',
            'altura',
            'exercicios',
        )
        read_only_fields = ('peso', 'altura', 'aluno')

    def validate_objetivo(self, value):
        valid = [choice[0] for choice in OBJETIVO_TREINO]
        if value not in valid:
            raise serializers.ValidationError(
                f"Objetivo inválido. Use um dos valores: {', '.join(valid)}"
            )
        return value

    def create(self, validated_data):
        """
        Cria um novo treino junto com seus exercícios associados.

        Valida se o aluno tem matrícula ativa e plano válido,
        e respeita o limite de treinos permitidos pelo plano.
        """
        print(f"🔄 Criando novo treino...")
        print(f"📋 Dados recebidos: {validated_data}")
        print(f"📋 Tipo dos dados: {type(validated_data)}")
        print(f"📋 Chaves disponíveis: {list(validated_data.keys())}")
        
        # Verificar especificamente o campo nome
        if 'nome' in validated_data:
            print(f"📝 Nome recebido: '{validated_data['nome']}'")
            print(f"📝 Tipo do nome: {type(validated_data['nome'])}")
            print(f"📝 Tamanho do nome: {len(validated_data['nome'])}")
        else:
            print("❌ Campo 'nome' NÃO encontrado nos dados")
        
        try:
            # Verificar se exercicios está presente
            if 'exercicios' not in validated_data:
                print("❌ Campo 'exercicios' não encontrado nos dados")
                raise serializers.ValidationError("Campo 'exercicios' é obrigatório")
            
            exercicios_data = validated_data.pop('exercicios')
            print(f"📋 Dados dos exercícios: {exercicios_data}")
            print(f"📋 Tipo dos exercícios: {type(exercicios_data)}")
            print(f"📋 Quantidade de exercícios: {len(exercicios_data) if exercicios_data else 0}")
            
            # Verificar se aluno está presente
            if 'aluno' not in validated_data:
                print("❌ Campo 'aluno' não encontrado nos dados")
                raise serializers.ValidationError("Campo 'aluno' é obrigatório")
            
            aluno = validated_data.get('aluno')
            print(f"👤 Aluno: {aluno}")
            print(f"👤 Tipo do aluno: {type(aluno)}")

            # Verificar se o aluno existe
            from cadastros.models import Aluno
            try:
                # Se o DRF já converteu para objeto, usar diretamente
                if isinstance(aluno, Aluno):
                    aluno_obj = aluno
                    aluno_id = aluno.id
                else:
                    # Se ainda é ID, buscar o objeto
                    aluno_obj = Aluno.objects.get(id=aluno)
                    aluno_id = aluno
                
                print(f"✅ Aluno encontrado: {aluno_obj.nome} (ID: {aluno_id})")
            except Aluno.DoesNotExist:
                print(f"❌ Aluno com ID {aluno} não existe")
                raise serializers.ValidationError(f"Aluno com ID {aluno} não existe")

            # Verifica se o aluno possui matrícula ativa
            matricula = Matricula.objects.filter(aluno=aluno_id, ativo=True).first()
            print(f"📋 Matrícula encontrada: {matricula}")
            
            if not matricula:
                print("❌ Aluno não possui matrícula ativa")
                raise serializers.ValidationError(
                    "Aluno não possui matrícula ativa.")

            # Verifica se a matrícula possui um plano válido
            if not matricula.plano or not matricula.plano.titulo:
                print("❌ Matrícula não tem plano válido")
                raise serializers.ValidationError(
                    "Matrícula não tem plano válido.")

            plano_titulo = matricula.plano.titulo.lower()
            print(f"📋 Plano: {plano_titulo}")

            # Define limites de treinos por plano
            limites = {
                'starter': 4,
                'dumbbell': 9999,  # ilimitado
            }
            # padrão bloqueia caso plano desconhecido
            limite = limites.get(plano_titulo, 0)
            print(f"📋 Limite de treinos: {limite}")

            # Conta os treinos existentes do aluno
            treinos_count = Treino.objects.filter(aluno=aluno_id, ativo=True).count()
            print(f"📋 Treinos existentes: {treinos_count}")
            
            if treinos_count >= limite:
                print(f"❌ Limite de treinos atingido: {treinos_count}/{limite}")
                raise serializers.ValidationError(
                    f"Você atingiu o limite de {limite} treinos para o seu plano '{plano_titulo}'."
                )

            # Cria o treino
            print(f"✅ Criando treino com dados: {validated_data}")
            try:
                treino = Treino.objects.create(**validated_data)
                print(f"✅ Treino criado com ID: {treino.id}")
                print(f"✅ Nome do treino salvo: '{treino.nome}'")
                print(f"✅ Verificando se o nome foi salvo corretamente...")
                
                # Recarregar o treino do banco para confirmar
                treino_refresh = Treino.objects.get(id=treino.id)
                print(f"✅ Nome após recarregar: '{treino_refresh.nome}'")
                
            except Exception as treino_error:
                print(f"❌ Erro ao criar treino: {treino_error}")
                print(f"❌ Tipo do erro: {type(treino_error)}")
                import traceback
                print(f"❌ Traceback do treino: {traceback.format_exc()}")
                raise

            # Cria os exercícios relacionados ao treino
            print(f"➕ Criando {len(exercicios_data)} exercícios...")
            for i, ex_data in enumerate(exercicios_data):
                print(f"📝 Criando exercício {i+1}: {ex_data}")
                try:
                    # Verificar se o exercício existe
                    exercicio_id = ex_data.get('exercicio')
                    if not Exercicio.objects.filter(id=exercicio_id).exists():
                        print(f"❌ Exercício com ID {exercicio_id} não existe")
                        raise serializers.ValidationError(f"Exercício com ID {exercicio_id} não existe")
                    
                    ExercicioTreino.objects.create(treino=treino, **ex_data)
                    print(f"✅ Exercício {i+1} criado com sucesso")
                except Exception as ex_error:
                    print(f"❌ Erro ao criar exercício {i+1}: {ex_error}")
                    print(f"❌ Tipo do erro: {type(ex_error)}")
                    import traceback
                    print(f"❌ Traceback do exercício: {traceback.format_exc()}")
                    raise serializers.ValidationError(f"Erro ao criar exercício: {str(ex_error)}")

            print(f"🎉 Treino criado com sucesso! ID: {treino.id}")
            return treino
            
        except Exception as e:
            print(f"❌ Erro durante criação do treino: {e}")
            print(f"❌ Tipo do erro: {type(e)}")
            import traceback
            print(f"❌ Traceback completo: {traceback.format_exc()}")
            raise

    def update(self, instance, validated_data):
        """
        Atualiza um treino existente, incluindo os exercícios associados.

        Se forem fornecidos novos exercícios, os antigos são removidos e substituídos.
        """
        print(f"🔄 Atualizando treino ID: {instance.id}")
        print(f"📋 Dados recebidos: {validated_data}")
        print(f"📋 Tipo dos dados: {type(validated_data)}")
        print(f"📋 Chaves disponíveis: {list(validated_data.keys())}")
        
        # Debug: verificar cada campo recebido
        for key, value in validated_data.items():
            print(f"🔍 Campo '{key}': '{value}' (tipo: {type(value)})")
        
        try:
            # Validar campo nome
            if 'nome' in validated_data:
                nome = validated_data['nome']
                print(f"📝 Nome recebido: '{nome}' (tipo: {type(nome)})")
                if not nome or nome.strip() == '':
                    print("❌ Nome está vazio")
                    raise serializers.ValidationError("Nome do treino não pode estar vazio")
                print(f"✅ Nome válido: {nome}")
            
            exercicios_data = validated_data.pop('exercicios', None)
            print(f"📋 Dados dos exercícios: {exercicios_data}")

            # Atualiza os campos do treino
            for attr, value in validated_data.items():
                print(f"📝 Atualizando campo {attr}: {value}")
                try:
                    setattr(instance, attr, value)
                    print(f"✅ Campo {attr} atualizado com sucesso")
                except Exception as field_error:
                    print(f"❌ Erro ao atualizar campo {attr}: {field_error}")
                    raise serializers.ValidationError(f"Erro ao atualizar campo {attr}: {str(field_error)}")
            
            print(f"💾 Salvando treino...")
            instance.save()
            print(f"✅ Treino atualizado: {instance}")
            print(f"✅ Nome final do treino: '{instance.nome}'")

            # Atualiza os exercícios se fornecidos
            if exercicios_data is not None:
                print(f"🗑️ Removendo exercícios antigos...")
                instance.exercicios.all().delete()
                print(f"➕ Criando novos exercícios...")
                for ex_data in exercicios_data:
                    print(f"📝 Criando exercício: {ex_data}")
                    try:
                        # Validar se o exercício existe
                        exercicio_id = ex_data.get('exercicio')
                        
                        # Se o DRF já converteu para objeto, usar o ID
                        if hasattr(exercicio_id, 'id'):
                            exercicio_id = exercicio_id.id
                        
                        print(f"🔍 Verificando exercício ID: {exercicio_id}")
                        if not Exercicio.objects.filter(id=exercicio_id).exists():
                            raise serializers.ValidationError(f"Exercício com ID {exercicio_id} não existe")
                        
                        # Preparar dados do exercício
                        exercicio_data = {
                            'exercicio': exercicio_id,
                            'series': ex_data.get('series'),
                            'repeticoes': ex_data.get('repeticoes'),
                            'carga': ex_data.get('carga'),
                            'descanso': ex_data.get('descanso')
                        }
                        
                        ExercicioTreino.objects.create(treino=instance, **exercicio_data)
                        print(f"✅ Exercício criado com sucesso")
                    except Exception as ex_error:
                        print(f"❌ Erro ao criar exercício: {ex_error}")
                        raise serializers.ValidationError(f"Erro ao criar exercício: {str(ex_error)}")

            return instance
        except Exception as e:
            print(f"❌ Erro durante atualização: {e}")
            print(f"❌ Tipo do erro: {type(e)}")
            import traceback
            print(f"❌ Traceback: {traceback.format_exc()}")
            raise serializers.ValidationError(f"Erro ao atualizar treino: {str(e)}")
