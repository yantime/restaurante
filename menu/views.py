from .models import Plato, Stock
from rest_framework.generics import ListCreateAPIView

from rest_framework import status 
from django.utils import timezone
from .permissions import soloAdminPuedeEscribir, soloMozoPuedeEscribir
from .serializers import PedidoSerializer, PlatoSerializer, StockCreateSerializer, StockSerializer,  AgregarDetallePedidoSerializer
from rest_framework.permissions import (AllowAny,  # sirve para que el controlador sea publico (no se necesite una token)
                                        # Los controladores soliciten una token de acceso
                                        IsAuthenticated,
                                        # Solamente para los metodos GET no sera necesaria la token pero para los demas metodos (POST, PUT, DELETE, PATCH) si sera requerido
                                        IsAuthenticatedOrReadOnly,
                                        # Verifica que en la token de acceso buscara al usuario y vera si es superuser (is_superuser)
                                        IsAdminUser,
                                        SAFE_METHODS,

                                        )
from rest_framework.response import Response
from rest_framework.request import Request
from cloudinary import CloudinaryImage
from factura.models import Pedido, DetallePedido
from django.db import IntegrityError, transaction


class PlatoApiView(ListCreateAPIView):
    serializer_class = PlatoSerializer
    queryset = Plato.objects.all()
    # sirve para indicar que tipos de permisos necesita el cliente para poder realizar la peticion
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request: Request):
        data = self.serializer_class(instance=self.get_queryset(), many=True)
        # hacer una iteracion para modificar la foto de cada plato y devolver el link de la foto
       
        # del contenido de la foto solamente extraer el nombre del archivo o si esta en una carpeta extraer la carpeta y el archivo
        link = CloudinaryImage(
            'plato/u3aj7qh0dtmy73yanv5j.jpg').image(secure=True)

        print(link)
        return Response(data=data.data)



class StockApiView(ListCreateAPIView):
    
    queryset = Stock.objects.all()
    permission_classes = [IsAuthenticated,soloAdminPuedeEscribir ]

    def get_serializer_class(self):
        if not self.request.method in SAFE_METHODS:
            return StockCreateSerializer    
        return StockSerializer
        





class PedidoApiView(ListCreateAPIView):
    serializer_class = PedidoSerializer  
    queryset = Pedido.objects.all()
    permission_classes = [IsAuthenticated, soloMozoPuedeEscribir ]

    def post(self, request: Request):
        print(request.user)
        request.data['usuario'] = request.user.id
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)
        data.save()
        return Response(data = data.data, status = status.HTTP_201_CREATED)



class AgregarDetallePedidoApiView(ListCreateAPIView):
    serializer_class = AgregarDetallePedidoSerializer
    queryset = DetallePedido.objects.all()
    

    def post(self, request: Request):
        # 1. valido la data con el serializer
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)
        # 2. verifico que tenga esa cantidad de productos en stock
        # SELECT * FROM stocks WHERE fecha = '...' AND plato_id = '...';
        stock :  stock | None  = Stock.objects.filter(fecha=timezone.now(),
                                     plato_id=data.validated_data.get('plato_id'),
                                     cantidad__gte = data.validated_data.get('cantidad')).first()
        
        if stock is None:
            return Response(data={'message': 'No hay stock para ese producto para el dia de hoy'},
                            status=status.HTTP_400_BAD_REQUEST) 

        pedido = Pedido.objects.filter(
            id=data.validated_data.get('pedido_id')).first()
        if pedido is None:
            return Response(data={'message': 'No hay ese pedido'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():    
                nuevoDetalle = DetallePedido(cantidad = data.validated_data.get('cantidad'), stock_id = stock, pedido_id = pedido)
                nuevoDetalle.save()
                
                stock.cantidad = stock.cantidad - nuevoDetalle.cantidad
                stock.save()

                pedido.total = pedido.total + (nuevoDetalle.cantidad * stock.precio_diario)
                pedido.save()
        except IntegrityError:
            return Response(data={'message': 'Error al crear el pedido, los cambios no se guardaron'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


        # verificar que en el stock este en base al dia de hoy esa cantidad
        # 3. agrego el detalle con su respectivo pedido
        return Response(data={'message': 'Detalle agregado exitosamente'})