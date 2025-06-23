# =============================================================================
# ARQUIVO: core/serializers.py
# DESCRIÇÃO: Serializers base e compartilhados do projeto Dumbbell Fitness
# FUNÇÃO: Define serializers reutilizáveis para User e EnderecoModel
# =============================================================================

# Import do pacote serializer do Django REST Framework
from rest_framework import serializers

# Import do modelo padrão User do Django
from django.contrib.auth.models import User

# Import do models Endereco do app core
from .models import EnderecoModel


class BaseUserSerializer(serializers.ModelSerializer):
    """
    Serializer base para User, que cuida do hash da senha no create e update.
    
    Este serializer é usado para gerenciar dados do usuário do Django de forma
    segura, garantindo que as senhas sejam sempre hasheadas antes de salvar.
    
    Funcionalidades:
    - Hash automático de senhas no create e update
    - Proteção contra exposição de senhas (write_only)
    - Reutilizável em outros serializers que precisam gerenciar User
    """
    class Meta:
        model = User  # Modelo User padrão do Django
        fields = '__all__'  # Todos os campos do modelo
        extra_kwargs = {
            'id': {'read_only': True},        # ID não pode ser editado
            'password': {'write_only': True}, # Senha nunca é retornada nas respostas
        }

    def create(self, validated_data):
        """
        Cria um novo usuário com senha hasheada.
        
        Este método é chamado quando um novo User é criado via API.
        Ele garante que a senha seja hasheada antes de salvar no banco.
        
        Args:
            validated_data (dict): Dados validados do usuário
            
        Returns:
            User: Instância do usuário criado
            
        Processo:
        1. Extrai a senha dos dados validados
        2. Cria o usuário sem a senha
        3. Define a senha hasheada usando set_password()
        4. Salva o usuário
        """
        # Extrai a senha dos dados validados (se existir)
        password = validated_data.pop('password', None)
        
        # Cria o usuário sem a senha
        user = self.Meta.model(**validated_data)
        
        # Se houver senha, define ela de forma segura (hash)
        if password:
            user.set_password(password)  # A magia do hash seguro
            
        # Salva o usuário no banco
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Atualiza um usuário existente com senha hasheada.
        
        Este método é chamado quando um User existente é atualizado via API.
        Ele garante que a senha seja hasheada se for fornecida.
        
        Args:
            instance (User): Instância atual do usuário
            validated_data (dict): Novos dados validados
            
        Returns:
            User: Instância do usuário atualizada
            
        Processo:
        1. Extrai a senha dos dados validados (se existir)
        2. Atualiza os demais campos
        3. Se houver nova senha, define ela de forma segura
        4. Salva as alterações
        """
        # Extrai a senha dos dados validados (se existir)
        password = validated_data.pop('password', None)
        
        # Atualiza os demais campos do usuário
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        # Se houver nova senha, define ela de forma segura
        if password:
            instance.set_password(password)  # Atualiza hash da senha
            
        # Salva as alterações no banco
        instance.save()
        return instance


class EnderecoSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo EnderecoModel.
    
    Gerencia a conversão de dados do modelo EnderecoModel para JSON e vice-versa.
    Inclui validações automáticas baseadas nos validadores definidos no modelo.
    
    Funcionalidades:
    - Validação automática de CEP (formato 99999-999)
    - Conversão de dados para/do formato JSON
    - Proteção do campo ID (read_only)
    - Verificação de endereços duplicados (evita criar endereços idênticos)
    """
    class Meta:
        model = EnderecoModel
        fields = ['id', 'cep', 'rua', 'numero', 'complemento', 'bairro', 'cidade', 'estado']
        extra_kwargs = {
            'id': {'read_only': True},  # ID é gerado automaticamente
        }

    def create(self, validated_data):
        """
        Cria um novo endereço ou retorna um existente se for idêntico.
        
        Este método verifica se já existe um endereço com os mesmos dados
        antes de criar um novo. Se encontrar um endereço idêntico, retorna
        o existente em vez de criar uma duplicata.
        
        Args:
            validated_data (dict): Dados validados do endereço
            
        Returns:
            EnderecoModel: Instância do endereço (novo ou existente)
            
        Processo:
        1. Busca por endereço existente com os mesmos dados
        2. Se encontrar, retorna o existente
        3. Se não encontrar, cria um novo
        """
        # Busca por endereço existente com os mesmos dados
        # Compara todos os campos exceto id, criacao, atualizacao e ativo
        endereco_existente = EnderecoModel.objects.filter(
            cep=validated_data.get('cep'),
            rua=validated_data.get('rua'),
            numero=validated_data.get('numero'),
            complemento=validated_data.get('complemento'),
            bairro=validated_data.get('bairro'),
            cidade=validated_data.get('cidade'),
            estado=validated_data.get('estado')
        ).first()
        
        # Se encontrar um endereço idêntico, retorna o existente
        if endereco_existente:
            return endereco_existente
        
        # Se não encontrar, cria um novo endereço
        return super().create(validated_data)

    def validate(self, data):
        """
        Validação customizada para o endereço.
        
        Pode ser usado para validações adicionais além das definidas
        no modelo, se necessário no futuro.
        
        Args:
            data (dict): Dados do endereço a serem validados
            
        Returns:
            dict: Dados validados
            
        Raises:
            ValidationError: Se a validação falhar
        """
        # Aqui podem ser adicionadas validações customizadas no futuro
        # Por exemplo, verificar se o CEP existe, validar endereço, etc.
        return data
