from django.contrib import admin
from .models import *
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent', 'status']
    list_filter = ['status']

class ProductImageInline(admin.TabularInline):
    model = Images
    extra = 5

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'image_tag']
    list_filter = ['category']
    readonly_fields = ('image_tag',)
    inlines = [ProductImageInline]
    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Images)