import csv
import openpyxl
from django.http import HttpResponse
from django import forms
from django.contrib import admin
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import Brand, Category, Product, UnitOfMeasurement, Entry, Exit
from django.core.exceptions import ValidationError

# Formulário personalizado para validação de saídas
class ExitForm(forms.ModelForm):
    class Meta:
        model = Exit
        fields = '__all__'

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        product = self.cleaned_data.get('product')

        if product and quantity > product.stock:
            raise forms.ValidationError(f"A quantidade não pode ser maior que o estoque disponível ({product.stock}).")
        
        return quantity

# Função para exportar como CSV
def export_as_csv(modeladmin, request, queryset):
    if not queryset:
        return HttpResponse("Nenhum item selecionado.")
    
    meta = modeladmin.model._meta
    field_names = [field.name for field in meta.fields if field.name != 'id']  # Excluindo o campo 'id'

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={meta.model_name}.csv'

    writer = csv.writer(response)
    writer.writerow(field_names)
    for obj in queryset:
        writer.writerow([getattr(obj, field) if getattr(obj, field) is not None else '' for field in field_names])

    return response

export_as_csv.short_description = "Exportar como CSV"

# Função para exportar como XLSX
def export_as_xlsx(modeladmin, request, queryset):
    if not queryset:
        return HttpResponse("Nenhum item selecionado.")
    
    meta = modeladmin.model._meta
    field_names = [field.name for field in meta.fields if field.name != 'id']  # Excluindo o campo 'id'

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = meta.model_name.capitalize()
    ws.append(field_names)

    for obj in queryset:
        row = []
        for field in field_names:
            value = getattr(obj, field)
            row.append(str(value) if hasattr(value, '__str__') else value if value is not None else '')  # Conversão para string se necessário
        ws.append(row)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={meta.model_name}.xlsx'
    wb.save(response)
    return response

export_as_xlsx.short_description = "Exportar como XLSX"

# Função para exportar como PDF
def export_as_pdf(modeladmin, request, queryset):
    if not queryset:
        return HttpResponse("Nenhum item selecionado.")
    
    meta = modeladmin.model._meta
    field_names = [field.name for field in meta.fields if field.name != 'id']  # Excluindo o campo 'id'

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={meta.model_name}.pdf'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, height - 40, f'{meta.model_name.capitalize()} - Exportação')

    p.setFont("Helvetica", 10)
    x_offset = 50
    y_offset = height - 60
    for i, field in enumerate(field_names):
        p.drawString(x_offset + i * 100, y_offset, field.capitalize())

    y_offset -= 20
    for obj in queryset:
        for i, field in enumerate(field_names):
            p.drawString(x_offset + i * 100, y_offset, str(getattr(obj, field)) if getattr(obj, field) is not None else '')
        y_offset -= 20

    p.showPage()
    p.save()

    return response

export_as_pdf.short_description = "Exportar como PDF"

# Registering Models in Django Admin

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at', 'updated_at']
    search_fields = ['name']
    list_filter = ['is_active']
    actions = [export_as_csv, export_as_xlsx, export_as_pdf]
    fieldsets = (
        (None, {'fields': ('name', 'is_active')}),
        ('Datas', {'fields': ('created_at', 'updated_at')})
    )
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at', 'updated_at']
    search_fields = ['name']
    list_filter = ['is_active']
    actions = [export_as_csv, export_as_xlsx, export_as_pdf]
    fieldsets = (
        (None, {'fields': ('name', 'is_active')}),
        ('Datas', {'fields': ('created_at', 'updated_at')})
    )
    readonly_fields = ['created_at', 'updated_at']

@admin.register(UnitOfMeasurement)
class UnitOfMeasurementAdmin(admin.ModelAdmin):
    list_display = ['name', 'symbol', 'is_active', 'created_at', 'updated_at']
    search_fields = ['name']
    list_filter = ['is_active']
    actions = [export_as_csv, export_as_xlsx, export_as_pdf]
    fieldsets = (
        (None, {'fields': ('name', 'symbol', 'is_active')}),
        ('Datas', {'fields': ('created_at', 'updated_at')})
    )
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'brand', 'category', 'price', 'stock', 'dimension',
        'unit_of_measurement', 'status', 'is_active', 'created_at', 'updated_at'
    ]
    search_fields = ['title', 'brand__name', 'category__name']
    list_filter = ['status', 'is_active', 'brand', 'category']
    actions = [export_as_csv, export_as_xlsx, export_as_pdf]
    fieldsets = (
        (None, {
            'fields': (
                'title', 'brand', 'category', 'price', 'stock',
                'dimension', 'unit_of_measurement', 'observation', 'status', 'is_active'
            )
        }),
        ('Datas', {'fields': ('created_at', 'updated_at')})
    )
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'quantity', 'date']
    search_fields = ['product__title', 'user__username']
    list_filter = ['date']
    readonly_fields = ['date']
    actions = [export_as_csv, export_as_xlsx, export_as_pdf]  # Adicionando ações de exportação

    def export_as_csv(self, request, queryset):
        return export_as_csv(self, request, queryset)

    def export_as_xlsx(self, request, queryset):
        return export_as_xlsx(self, request, queryset)

    def export_as_pdf(self, request, queryset):
        return export_as_pdf(self, request, queryset)

@admin.register(Exit)
class ExitAdmin(admin.ModelAdmin):
    form = ExitForm  # Usando o formulário personalizado
    list_display = ['product', 'user', 'quantity', 'date']
    search_fields = ['product__title', 'user__username']
    list_filter = ['date']
    readonly_fields = ['date']
    actions = [export_as_csv, export_as_xlsx, export_as_pdf]  # Adicionando ações de exportação

    def export_as_csv(self, request, queryset):
        return export_as_csv(self, request, queryset)

    def export_as_xlsx(self, request, queryset):
        return export_as_xlsx(self, request, queryset)

    def export_as_pdf(self, request, queryset):
        return export_as_pdf(self, request, queryset)

    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            # Adiciona uma mensagem de erro ao admin
            self.message_user(request, str(e), level='error')