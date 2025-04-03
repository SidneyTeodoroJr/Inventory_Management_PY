# Generated by Django 5.1.7 on 2025-03-12 17:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_product_unit_of_measurement'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnitOfMeasurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Unidade de Medida')),
                ('symbol', models.CharField(blank=True, max_length=10, null=True, verbose_name='Símbolo')),
                ('is_active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
            ],
            options={
                'verbose_name': 'Unidade de Medida',
                'verbose_name_plural': 'Unidades de Medida',
                'ordering': ['name'],
            },
        ),
        migrations.AlterField(
            model_name='product',
            name='unit_of_measurement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='products.unitofmeasurement', verbose_name='Un. de Medida'),
        ),
    ]
