from rest_framework import serializers
from .models import Vendedor
from .models import Produto

class VendedorSerializer(serializers.ModelSerializer):
    vendas_realizadas = serializers.ReadOnlyField()
    class Meta:
        model = Vendedor
        fields = ['id', 'nome', 'sobrenome', 'email', 'telefone', 'endereco', 'data_contratacao', 'vendas_realizadas']
        
        def update(self, instance, validated_data):
            vendedor = Vendedor.objects.filter(id=instance.id).first()
            if 'id' in validated_data and instance.id != validated_data['id']:
                status = instance.venda_set.filter(status='entregue').exists()
                if status:
                    raise serializers.ValidationError("Não é possível alterar um vendedor que já realizou entregas.")

            instance.nome = validated_data.get('nome', instance.nome)
            instance.sobrenome = validated_data.get('sobrenome', instance.sobrenome)
            instance.email = validated_data.get('email', instance.email)
            instance.telefone = validated_data.get('telefone', instance.telefone)
            instance.endereco = validated_data.get('endereco', instance.endereco)
            instance.data_contratacao = validated_data.get('data_contratacao', instance.data_contratacao)
            instance.save()
            return instance
        
class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['id', 'cliente', 'vendedor', 'data_pedido', 'status', 'total']