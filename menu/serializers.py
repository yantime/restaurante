from factura.models import Pedido
from rest_framework import serializers
from .models import Plato, Stock


class PlatoSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Plato

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Stock
        depth = 1

class StockCreateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Stock
       


class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Pedido
     

class AgregarDetallePedidoSerializer(serializers.Serializer):
    cantidad = serializers.IntegerField(min_value=1)
    pedido_id = serializers.IntegerField(min_value=1)
    plato_id = serializers.IntegerField(min_value=1)