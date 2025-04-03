from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nome')
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        ordering = ['name']
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'

    def __str__(self):
        return self.name
    

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nome')
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        ordering = ['name']
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.name
    

class UnitOfMeasurement(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Símbolo')
    symbol = models.CharField(max_length=10, verbose_name='Unidade de Medida', blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        ordering = ['name']
        verbose_name = 'Unidade de Medida'
        verbose_name_plural = 'Un. de medida'

    def __str__(self):
        return self.name


class Product(models.Model):
    STATUS_CHOICES = [
        ('in_stock', 'Em Estoque'),
        ('temporarily_unavailable', 'Indisponível'),
        ('out_of_stock', 'Esgotado'),
    ]

    title = models.CharField(max_length=100, verbose_name='Título')
    brand = models.ForeignKey(
        Brand, on_delete=models.PROTECT, verbose_name='Marca', related_name='products', blank=True, null=True
    )
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, verbose_name='Categoria', related_name='products'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço')
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    dimension = models.CharField(max_length=100, verbose_name='Dimensão', blank=True, null=True)
    stock = models.IntegerField(verbose_name='Estoque Atual', default=0)
    unit_of_measurement = models.ForeignKey(
        UnitOfMeasurement, on_delete=models.PROTECT, verbose_name='Un. de Medida'
    )
    observation = models.TextField(verbose_name='Observação', blank=True, null=True)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default='in_stock', verbose_name='Status'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        ordering = ['title']
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        brand_name = self.brand.name if self.brand else "Sem Marca"
        category_name = self.category.name if self.category else "Sem Categoria"
        return f"{self.title} ({brand_name} - {category_name})"

    def save(self, *args, **kwargs):
        # Atualiza o status com base no estoque
        if self.stock <= 0:
            self.status = 'out_of_stock'
        elif self.status == 'out_of_stock' and self.stock > 0:
            self.status = 'in_stock'
        
        # Chama o método save da superclasse
        super().save(*args, **kwargs)


class Entry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Produto')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    quantity = models.PositiveIntegerField(verbose_name='Quantidade')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Data')

    class Meta:
        ordering = ['-date']
        verbose_name = 'Entrada'
        verbose_name_plural = 'Entradas'

    def clean(self):
        if self.quantity is None or self.quantity <= 0:
            raise ValidationError("A quantidade de entrada deve ser maior que 0.")
        if not self.product.is_active:
            raise ValidationError("Não é possível adicionar entradas para produtos que não estão ativos.")

    def save(self, *args, **kwargs):
        # Chama a validação antes de salvar
        self.clean()

        # Atualiza o estoque do produto
        self.product.stock += self.quantity  # Adiciona ao estoque
        self.product.save()

        # Chama o método save da superclasse
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Entrada de {self.quantity} {self.product.unit_of_measurement.symbol} de {self.product.title} por {self.user.username}"


class Exit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Produto')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    quantity = models.PositiveIntegerField(verbose_name='Quantidade')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Data')

    class Meta:
        ordering = ['-date']
        verbose_name = 'Saída'
        verbose_name_plural = 'Saídas'

    def clean(self):
        if self.quantity is None or self.quantity <= 0:
            raise ValidationError("A quantidade de saída deve ser maior que 0.")
        if self.product.status == 'temporarily_unavailable':
            raise ValidationError("Não é possível retirar produtos que estão indisponíveis.")
        if not self.product.is_active:
            raise ValidationError("Não é possível retirar produtos que não estão ativos.")
        if self.quantity > self.product.stock:
            raise ValidationError(f"Não é possível sair mais do que o estoque disponível ({self.product.stock}).")

    def save(self, *args, **kwargs):
        # Chama a validação antes de salvar
        self.clean()

        # Atualiza o estoque do produto
        self.product.stock -= self.quantity  # Subtrai do estoque
        self.product.save()

        # Chama o método save da superclasse
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Saída de {self.quantity} {self.product.unit_of_measurement.symbol} de {self.product.title} por {self.user.username}"