# Generated by Django 4.2 on 2024-05-31 04:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_customer_invoice_product_cost_product_iva_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supplier', to='core.supplier', verbose_name='Proveedor'),
        ),
    ]
