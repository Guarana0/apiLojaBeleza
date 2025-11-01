from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Venda, ItemPedido

@receiver(post_save, sender=Venda)
def atualizar_detalhes_venda(sender, instance, created, **kwargs):
    if created:
        total_venda = 0
        for item in instance.itens.all():
            # Garante que o preco_unitario seja definido se estiver faltando
            if not item.preco_unitario:
                item.preco_unitario = item.produto.preco
            
            # Calcula o total do item
            total_item = item.preco_unitario * item.quantidade
            total_venda += total_item
            
            # Atualiza o estoque do produto
            produto = item.produto
            if produto.estoque < item.quantidade:
                # Esta validação é um fallback, o ideal é validar no serializer.
                # Por simplicidade aqui, vamos apenas registrar ou lançar um erro.
                # No nosso caso, a venda será revertida pela transação do banco de dados se falhar.
                raise Exception(f"Estoque insuficiente para o produto: {produto.nome}")
            
            produto.estoque -= item.quantidade
            produto.save(update_fields=['estoque'])
            item.save(update_fields=['preco_unitario'])

        # Atualiza o total da venda
        instance.total = total_venda
        instance.save(update_fields=['total'])
        
        # Atualiza a fatura do cliente
        instance.cliente.atualizar_fatura()
