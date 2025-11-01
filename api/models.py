from django.db import models
from django.db.models import Sum
from config import settings

# Create your models here.
class Vendedor(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15)
    endereco = models.CharField(max_length=255)
    data_contratacao = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nome} {self.sobrenome}"
    
    @property
    def vendas_realizadas(self):
        return self.vendas.count()
    
class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15)
    endereco = models.CharField(max_length=255)
    fatura = models.DecimalField(max_digits=10, decimal_places=2)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nome} {self.sobrenome}"
    
    def get_full_address(self):
        return self.endereco
    
    @property
    def produtos_comprados(self):
    # Soma a quantidade de todos os itens em todos os pedidos do cliente
        total_itens = self.pedidos.aggregate(
            total=Sum('itens__quantidade')
        )['total']
        return total_itens if total_itens is not None else 0

    def atualizar_fatura(self):
        # Soma o total de todos os pedidos (vendas) associados a este cliente
        total_pedidos = self.pedidos.aggregate(
            total_fatura=Sum('total')
        )['total_fatura']
        
        self.fatura = total_pedidos if total_pedidos is not None else 0.00
        self.save(update_fields=['fatura'])
    
class Venda(models.Model): 
    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Entregue', 'Entregue'),
        ('Cancelado', 'Cancelado'),
    ]

    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='pedidos')
    vendedor = models.ForeignKey(Vendedor, on_delete=models.SET_NULL, null=True, blank=True, related_name='vendas')
    data_pedido = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pendente')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente}"

    def calcular_total(self):
        total_price = sum(item.get_total() for item in self.itens.all())
        self.total = total_price
        self.save()
        return total_price
    
    
class Produto(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField()
    categoria = models.CharField(max_length=100)
    data_adicao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nome
    
    def is_in_stock(self):
        return self.estoque > 0

    
class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Venda, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, blank=True) # Price at the time of order

    def save(self, *args, **kwargs):
        if not self.preco_unitario:
            self.preco_unitario = self.produto.preco
        super().save(*args, **kwargs)

    def get_total(self):
        return self.preco_unitario * self.quantidade

    def __str__(self):
        return f"{self.quantidade} x {self.produto.nome}"