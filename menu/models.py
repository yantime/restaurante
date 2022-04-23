from django.db import models
from cloudinary import models as modelsCloudinary


class Plato(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45, null=False)
    foto = modelsCloudinary.CloudinaryField('plato', folder='restaurante/menu')
    disponible = models.BooleanField(default=True, null=False)
    precio = models.FloatField(null=False)

    class Meta:
        db_table = 'platos'

class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateField(null=False)
    cantidad = models.IntegerField(null=False)
    precio_diario = models.FloatField(null=False)

    plato_id = models.ForeignKey(Plato, on_delete=models.CASCADE, related_name='stocks', db_column='plato_id' )

    class Meta:
        db_table = 'stock'

        unique_together = (['fecha', 'plato_id'],)