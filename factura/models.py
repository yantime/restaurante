from django.db import models
from autorizacion.models import Usuario
from menu.models import Stock
from django.utils import timezone

# Create your models here.

class Pedido(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateTimeField( default=timezone.now)
    total = models.FloatField(null=False)
    numeroDocumentoCliente = models.CharField(max_length=12, null=True)
    tipoDocumentoCliente = models.CharField(
        choices=(['RUC', 'RUC'], ['DNI', 'DNI']), max_length=5, null=True)
    mesa = models.IntegerField( null=False)
    propina = models.FloatField()
    usuario = models.ForeignKey(to = Usuario, on_delete=models.CASCADE, related_name='pedidos', db_column='usuario_id')

    class Meta:
        db_table = 'pedidos'


class Comprobante(models.Model):
    id = models.AutoField(primary_key=True)
    serie = models.CharField(max_length=5, null=False)
    numero = models.CharField(max_length=10, null=False)
    pdf = models.TextField()
    cdr = models.TextField()
    xml = models.TextField()
    tipo = models.CharField(choices=(['BOLETA', 'BOLETA'], [
                            'FACTURA', 'FACTURA']), null=False, max_length=10)

    pedido = models.OneToOneField(to = Pedido, on_delete=models.CASCADE, related_name='comprobante', db_column='pedido_id')

    class Meta:
        db_table = 'comprobantes'
        unique_together = [['serie', 'numero']]



class DetallePedido(models.Model):
    id = models.AutoField(primary_key=True)
    cantidad = models.FloatField(null=False)
    stock_id = models.ForeignKey(to = Stock, on_delete=models.CASCADE, related_name='detalle_pedidos', db_column='stock_id')
    pedido_id = models.ForeignKey(to = Pedido, on_delete=models.CASCADE, related_name='detalle_pedidos', db_column='pedido_id')

    class Meta:
        db_table = 'detalle_pedidos'
        