from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from .models import Vendedor
from .models import Venda
from .models import Cliente
from .models import ItemPedido
from .models import Produto

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['id', 'nome', 'descricao', 'preco', 'estoque', 'categoria', 'data_adicao', 'data_atualizacao', 'ativo']
        read_only_fields =  ['data_adicao', 'data_atualizacao', 'ativo']
        
        def create(self, validated_data):
            estoque = validated_data.get('estoque', 0)
            if estoque <= 0:
                validated_data['ativo'] = False
            else:
                validated_data['ativo'] = True
            
            produto = super().create(validated_data)
            return produto


class VendedorSerializer(serializers.ModelSerializer):
    vendas_realizadas = serializers.ReadOnlyField()
    class Meta:
        model = Vendedor
        fields = ['id', 'nome', 'sobrenome', 'email', 'telefone', 'endereco', 'data_contratacao', 'vendas_realizadas']
        
    def update(self, instance, validated_data):
        if instance.vendas.filter(status='Entregue').exists():
                raise serializers.ValidationError("Não é possível alterar um vendedor que já realizou entregas.")
            
        return super().update(instance, validated_data)
    
class ClienteSerializer(serializers.ModelSerializer):
    produtos_comprados = serializers.ReadOnlyField()
    class Meta:
        model = Cliente
        fields = ['id', 'nome', 'sobrenome', 'email', 'telefone', 'endereco', 'fatura', 'produtos_comprados', 'data_cadastro']
        read_only_fields = ['produtos_comprados', 'fatura']
        
        def create(self, validated_data):
            validated_data['fatura'] = 0
            return super().create(validated_data)
        
class ItemPedidoSerializer(serializers.ModelSerializer):
    # Para leitura (GET), exibe todos os detalhes do produto.
    produto = ProdutoSerializer(read_only=True)
    # Para escrita (POST), espera apenas o ID do produto.
    produto_id = serializers.PrimaryKeyRelatedField(
        queryset=Produto.objects.all(), source='produto', write_only=True
    )

    class Meta:
        model = ItemPedido
        fields = ['produto', 'produto_id', 'quantidade']
        
      
class VendaSerializer(WritableNestedModelSerializer):
    itens = ItemPedidoSerializer(many=True)
    cliente = serializers.StringRelatedField(read_only=True)
    cliente_id = serializers.PrimaryKeyRelatedField(
        queryset=Cliente.objects.all(), source='cliente', write_only=True
    )
    
    class Meta:
        model = Venda
        fields = ['id', 'cliente', 'cliente_id', 'vendedor', 'data_pedido', 'status', 'total', 'itens']
        read_only_fields = ['total', 'data_pedido', 'status', 'cliente']