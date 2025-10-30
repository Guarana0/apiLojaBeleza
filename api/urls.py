from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VendedorViewSet
from .views import ProdutoViewSet

router = DefaultRouter()

#/api/vendedores/ get e post
#/api/vendedores/{id}/ get, patch, delete e put
router.register(r'vendedores', VendedorViewSet, basename='vendedor')

router.register(r'produtos', ProdutoViewSet, basename='produtos')

urlpatterns = [
    path('', include(router.urls)),
]