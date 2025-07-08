from django.contrib import admin
from .models import *

class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock_quantity', 'expiry_date')
    list_filter = ('category', 'expiry_date')
    search_fields = ('name', 'description')
    date_hierarchy = 'expiry_date'

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'total_amount', 'payment_method', 'purchase_date')
    list_filter = ('payment_method', 'purchase_date')
    search_fields = ('customer_name', 'customer_phone')
    date_hierarchy = 'purchase_date'
    inlines = [PurchaseItemInline]

@admin.register(PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):
    list_display = ('purchase', 'medication', 'quantity', 'unit_price', 'subtotal')
    list_filter = ('purchase__purchase_date',)
    search_fields = ('medication__name',)

@admin.register(Medicament)
class MedicamentAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix', 'dosage', 'forme', 'laboratoire', 'is_active', 'created_at')
    list_filter = ('is_active', 'forme', 'laboratoire')
    search_fields = ('nom', 'laboratoire')
