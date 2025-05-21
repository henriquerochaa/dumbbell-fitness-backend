from rest_framework import serializers
from .models import Treino, ExercicioTreino
from exercicios.models import Exercicio


class ExercicioTreinoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExercicioTreino
        fields = (
            'id',
            'exercicio',
            'series',
            'repeticoes',
            'carga',
            'descanso',
        )


class TreinoSerializer(serializers.ModelSerializer):
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
        exercicios_data = validated_data.pop('exercicios')
        aluno = validated_data['aluno']

        # Conta quantos treinos o aluno já tem
        treinos_count = Treino.objects.filter(aluno=aluno).count()

        # Define limites de acordo com o nome do plano (ajuste conforme seu modelo)
        plano_nome = aluno.plano.nome.lower() if aluno.plano else ''
        limites = {
            'starter': 4,
            'dumbbell': 9999,  # ilimitado
        }
        limite = limites.get(plano_nome, 0)  # 0 bloqueia por padrão

        if treinos_count >= limite:
            raise serializers.ValidationError(
                f"Você atingiu o limite de {limite} treinos para o seu plano '{plano_nome}'."
            )

        treino = Treino.objects.create(**validated_data)
        for ex_data in exercicios_data:
            ExercicioTreino.objects.create(treino=treino, **ex_data)
        return treino

    def update(self, instance, validated_data):
        exercicios_data = validated_data.pop('exercicios', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if exercicios_data is not None:
            instance.exercicios.all().delete()
            for ex_data in exercicios_data:
                ExercicioTreino.objects.create(treino=instance, **ex_data)

        return instance
