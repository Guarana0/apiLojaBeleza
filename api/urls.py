from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VendedorViewSet, ClienteViewSet, ItemPedidoViewSet, VendaViewSet, ProdutoViewSet

router = DefaultRouter()

#/api/vendedores/ get e post
#/api/vendedores/{id}/ get, patch, delete e put
router.register(r'vendedores', VendedorViewSet, basename='vendedor')

router.register(r'clientes', ClienteViewSet, basename='clientes')

router.register(r'itemPedido', ItemPedidoViewSet, basename='itemPedidos')

router.register(r'venda', VendaViewSet, basename='vendas')

router.register(r'produto', ProdutoViewSet, basename='produtos')

urlpatterns = [
    path('', include(router.urls)),
]