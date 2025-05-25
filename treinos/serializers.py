from rest_framework import serializers
from .models import Treino, ExercicioTreino
from exercicios.models import Exercicio
from cadastros.models import Matricula

class ExercicioTreinoSerializer(serializers.ModelSerializer):
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
        aluno = validated_data.get('aluno')

        # Confere se tem matrícula
        matricula = Matricula.objects.filter(aluno=aluno).first()
        if not matricula:
            raise serializers.ValidationError("Aluno não possui matrícula ativa.")

        # Confere se matrícula tem plano válido
        if not matricula.plano or not matricula.plano.nome:
            raise serializers.ValidationError("Matrícula não tem plano válido.")

        plano_nome = matricula.plano.nome.lower()

        limites = {
            'starter': 4,
            'dumbbell': 9999,  # ilimitado
        }
        limite = limites.get(plano_nome, 0)  # 0 bloqueia por padrão

        treinos_count = Treino.objects.filter(aluno=aluno).count()
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
