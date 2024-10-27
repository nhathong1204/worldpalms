from django.contrib import admin
from core.models import Product, Category, ProductImages

# Register your models here.
class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['user','pid','title','product_description','product_image','price','product_status']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title','category_image']

    
admin.site.register(Product,ProductAdmin)
admin.site.register(Category,CategoryAdmin)