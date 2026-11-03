from django.contrib import admin
from foodapp.models import Category,FoodItem

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','category_name']


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display=['id','food_name','price','category']
    search_fields=['food_name']
    list_filter=['category']
    list_editable = ['price', 'category']