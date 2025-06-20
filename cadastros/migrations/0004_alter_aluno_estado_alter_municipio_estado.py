# Generated by Django 5.2 on 2025-05-24 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0003_alter_aluno_estado_alter_municipio_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aluno',
            name='estado',
            field=models.CharField(choices=[('P', 'Paraná'), ('S', 'São Paulo'), ('G', 'Goiânia'), ('D', 'Distrito Federal')], max_length=40, verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='municipio',
            name='estado',
            field=models.CharField(choices=[('P', 'Paraná'), ('S', 'São Paulo'), ('G', 'Goiânia'), ('D', 'Distrito Federal')], max_length=40, verbose_name='Estado'),
        ),
    ]
