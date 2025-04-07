import csv
import openpyxl

from django.http import HttpResponse
from django import forms
from django.contrib import admin, messages
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import Brand, Category, Product, UnitOfMeasurement, Entry, Exit
from django.core.exceptions import ValidationError
from django.contrib.admin.models import LogEntry


# Habilita a exclusão do LogEntry pelo Admin
@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['action_time', 'user', 'content_type', 'object_repr', 'action_flag']
    search_fields = ['user__username', 'object_repr']
    list_filter = ['action_flag', 'content_type', 'user']
    readonly_fields = ['action_time', 'user', 'content_type', 'object_repr', 'object_id', 'change_message']
    actions = ['excluir_logs_selecionados', 'delete_all_logs']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

    def delete_queryset(self, request, queryset):
        queryset.delete()

    def excluir_logs_selecionados(self, request, queryset):
        self.delete_queryset(request, queryset)
        self.message_user(request, "Logs selecionados excluídos com sucesso!", level=messages.SUCCESS)
    excluir_logs_selecionados.short_description = "🗑️ Excluir logs selecionados"


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
    field_names = [field.name for field in meta.fields if field.name != 'id']

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
    field_names = [field.name for field in meta.fields if field.name != 'id']

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = meta.model_name.capitalize()
    ws.append(field_names)

    for obj in queryset:
        row = []
        for field in field_names:
            value = getattr(obj, field)
            row.append(str(value) if hasattr(value, '__str__') else value if value is not None else '')
        ws.append(row)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={meta.model_name}.xlsx'
    wb.save(response)
    return response

export_as_xlsx.short_description = "Exportar como XLSX"


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at', 'updated_at']
    search_fields = ['name']
    list_filter = ['is_active']
    actions = [export_as_csv, export_as_xlsx]
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
    actions = [export_as_csv, export_as_xlsx]
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
    actions = [export_as_csv, export_as_xlsx]
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
    actions = [export_as_csv, export_as_xlsx]
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
    actions = [export_as_csv, export_as_xlsx]

    def export_as_csv(self, request, queryset):
        return export_as_csv(self, request, queryset)

    def export_as_xlsx(self, request, queryset):
        return export_as_xlsx(self, request, queryset)


@admin.register(Exit)
class ExitAdmin(admin.ModelAdmin):
    form = ExitForm
    list_display = ['product', 'user', 'quantity', 'date']
    search_fields = ['product__title', 'user__username']
    list_filter = ['date']
    readonly_fields = ['date']
    actions = [export_as_csv, export_as_xlsx]

    def export_as_csv(self, request, queryset):
        return export_as_csv(self, request, queryset)

    def export_as_xlsx(self, request, queryset):
        return export_as_xlsx(self, request, queryset)

    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            self.message_user(request, str(e), level='error')