# Generated by Django 4.2 on 2024-05-31 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_supplier_phone_alter_supplier_ruc'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='brand',
            name='core_brand_descrip_5b1a81_idx',
        ),
        migrations.AlterField(
            model_name='brand',
            name='description',
            field=models.CharField(max_length=100, unique=True, verbose_name='Articulo'),
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.CharField(max_length=100, unique=True, verbose_name='Categoria'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(max_length=100, unique=True, verbose_name='Articulo'),
        ),
    ]
