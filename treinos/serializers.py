from rest_framework import serializers
from .models import Treino, ExercicioTreino
from exercicios.models import Exercicio
from cadastros.models import Matricula


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
            'aluno',
            'objetivo',
            'disponibilidade',
            'observacao',
            'peso',
            'altura',
            'exercicios',
        )
        read_only_fields = ('peso', 'altura')

    def create(self, validated_data):
        """
        Cria um novo treino junto com seus exercícios associados.

        Valida se o aluno tem matrícula ativa e plano válido,
        e respeita o limite de treinos permitidos pelo plano.
        """
        exercicios_data = validated_data.pop('exercicios')
        aluno = validated_data.get('aluno')

        # Verifica se o aluno possui matrícula ativa
        matricula = Matricula.objects.filter(aluno=aluno).first()
        if not matricula:
            raise serializers.ValidationError(
                "Aluno não possui matrícula ativa.")

        # Verifica se a matrícula possui um plano válido
        if not matricula.plano or not matricula.plano.nome:
            raise serializers.ValidationError(
                "Matrícula não tem plano válido.")

        plano_nome = matricula.plano.nome.lower()

        # Define limites de treinos por plano
        limites = {
            'starter': 4,
            'dumbbell': 9999,  # ilimitado
        }
        # padrão bloqueia caso plano desconhecido
        limite = limites.get(plano_nome, 0)

        # Conta os treinos existentes do aluno
        treinos_count = Treino.objects.filter(aluno=aluno).count()
        if treinos_count >= limite:
            raise serializers.ValidationError(
                f"Você atingiu o limite de {limite} treinos para o seu plano '{plano_nome}'."
            )

        # Cria o treino
        treino = Treino.objects.create(**validated_data)

        # Cria os exercícios relacionados ao treino
        for ex_data in exercicios_data:
            ExercicioTreino.objects.create(treino=treino, **ex_data)

        return treino

    def update(self, instance, validated_data):
        """
        Atualiza um treino existente, incluindo os exercícios associados.

        Se forem fornecidos novos exercícios, os antigos são removidos e substituídos.
        """
        exercicios_data = validated_data.pop('exercicios', None)

        # Atualiza os campos do treino
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Atualiza os exercícios se fornecidos
        if exercicios_data is not None:
            instance.exercicios.all().delete()
            for ex_data in exercicios_data:
                ExercicioTreino.objects.create(treino=instance, **ex_data)

        return instance
