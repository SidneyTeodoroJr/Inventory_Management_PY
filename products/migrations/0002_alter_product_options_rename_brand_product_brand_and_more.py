# Generated by Django 5.1.7 on 2025-03-12 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['title'], 'verbose_name': 'Produto'},
        ),
        migrations.RenameField(
            model_name='product',
            old_name='Brand',
            new_name='brand',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='Category',
            new_name='category',
        ),
        migrations.RemoveField(
            model_name='brand',
            name='description',
        ),
        migrations.RemoveField(
            model_name='category',
            name='description',
        ),
        migrations.RemoveField(
            model_name='product',
            name='description',
        ),
        migrations.AddField(
            model_name='product',
            name='dimension',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Dimensão'),
        ),
        migrations.AddField(
            model_name='product',
            name='observation',
            field=models.TextField(blank=True, null=True, verbose_name='Observação'),
        ),
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('in_stock', 'Em Estoque'), ('temporarily_unavailable', 'Indisponível'), ('out_of_stock', 'Esgotado')], default='in_stock', max_length=50, verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.IntegerField(default=0, verbose_name='Estoque Atual'),
        ),
        migrations.AddField(
            model_name='product',
            name='unit_of_measurement',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Un. de Medida'),
        ),
    ]
