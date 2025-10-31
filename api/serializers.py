from rest_framework import serializers
from .models import Vendedor
from .models import Venda
from .models import Cliente
from .models import ItemPedido
from .models import Produto

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
        read_only_fields = ['fatura', 'produtos_comprados']
        
        def update(self, validate_data):
            produto_comprado = []
            produto_comprado.append[Produto]
        
class ItemPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPedido
        fields = ['produto', 'quantidade']
        
class ItemPedidoDetalheSerializer(serializers.ModelSerializer):
    produto = serializers.StringRelatedField()
    class Meta:
        model = ItemPedido
        fields = ['produto', 'quantidade', 'preco_unitario']
        
# codigo feito com IA, provavelmente deve dar para melhorar        
class VendaSerializer(serializers.ModelSerializer):
    itens = ItemPedidoSerializer(many=True, write_only=True)
    itens_detalhe = ItemPedidoDetalheSerializer(source='itens', many=True, read_only=True)
    cliente = serializers.StringRelatedField(read_only=True)
    # Para criar (POST): Recebe o ID do cliente. É mais eficiente e seguro.
    cliente_id = serializers.PrimaryKeyRelatedField(
        queryset=Cliente.objects.all(), source='cliente', write_only=True
    )
    
    class Meta:
        model = Venda
        fields = ['id', 'cliente', 'cliente_id', 'vendedor', 'data_pedido', 'status', 'total', 'itens', 'itens_detalhe']
        read_only_fields = ['total', 'data_pedido', 'status']
        
        def create(self, validated_data):
            itens_data = validated_data.pop('itens')
            venda = Venda.objects.create(**validated_data)
            
            total_venda = 0
            
            for item_data in itens_data:
                produto = item_data['produto']
                quantidade = item_data['quantidade']

                if produto.estoque < quantidade:
                    venda.delete()
                    raise serializers.ValidationError('Não temos essa quantidade do produto no estoque')
                
                ItemPedido.objects.create(
                    pedido=venda,
                    produto=produto,
                    quantidade=quantidade,
                    preco_unitario=produto.preco
                )
                total_venda += produto.preco * quantidade
                produto.estoque -= quantidade
                produto.save()
            
            venda_total = total_venda
            venda.save()
            
            venda.cliente.atualizar_fatura()
            
            return venda

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

    