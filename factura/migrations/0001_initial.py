# Generated by Django 4.0.4 on 2022-04-19 02:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('menu', '0003_stock'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateTimeField()),
                ('total', models.FloatField()),
                ('numeroDocumentoCliente', models.CharField(max_length=12)),
                ('tipoDocumentoCliente', models.CharField(choices=[['RUC', 'RUC'], ['DNI', 'DNI']], max_length=5)),
                ('mesa', models.IntegerField()),
                ('propina', models.FloatField()),
                ('usuario', models.ForeignKey(db_column='usuario_id', on_delete=django.db.models.deletion.CASCADE, related_name='pedidos', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'pedidos',
            },
        ),
        migrations.CreateModel(
            name='DetallePedido',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.FloatField()),
                ('pedido_id', models.ForeignKey(db_column='pedido_id', on_delete=django.db.models.deletion.CASCADE, related_name='detalle_pedidos', to='factura.pedido')),
                ('stock_id', models.ForeignKey(db_column='stock_id', on_delete=django.db.models.deletion.CASCADE, related_name='detalle_pedidos', to='menu.stock')),
            ],
            options={
                'db_table': 'detalle_pedidos',
            },
        ),
        migrations.CreateModel(
            name='Comprobante',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('serie', models.CharField(max_length=5)),
                ('numero', models.CharField(max_length=10)),
                ('pdf', models.TextField()),
                ('cdr', models.TextField()),
                ('xml', models.TextField()),
                ('tipo', models.CharField(choices=[['BOLETA', 'BOLETA'], ['FACTURA', 'FACTURA']], max_length=10)),
                ('pedido', models.OneToOneField(db_column='pedido_id', on_delete=django.db.models.deletion.CASCADE, related_name='comprobante', to='factura.pedido')),
            ],
            options={
                'db_table': 'comprobantes',
                'unique_together': {('serie', 'numero')},
            },
        ),
    ]
