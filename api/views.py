from django.shortcuts import render
from rest_framework import viewsets

from .serializers import VendedorSerializer
from .serializers import ProdutoSerializer

from .models import Vendedor
from .models import Produto

class VendedorViewSet(viewsets.ModelViewSet):
    queryset = Vendedor.objects.all()
    serializer_class = VendedorSerializer
    
class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Vendedor.objects.all()
    serializer_class = ProdutoSerializer