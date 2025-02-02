from rest_framework import serializers
from .models import Category,Subcategory,Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubcategorySerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()  # Using a method to fetch category details

    class Meta:
        model = Subcategory
        fields = ["id", "name", "image", "is_active", "category", "category_name"]  # Includes category ID + details

    def get_category_name(self, obj):
        return obj.category.name
    
class ProductSerializer(serializers.ModelSerializer):
    # Using SerializerMethodField to get subcategory name and category name
    subcategory_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "name", "image", "is_active", "subcategory", "subcategory_name", "category_name"]

    def get_subcategory_name(self, obj):
        # Access the subcategory name of the product
        return obj.subcategory.name if obj.subcategory else None

    def get_category_name(self, obj):
        # Access the category name of the subcategory associated with the product
        return obj.subcategory.category.name if obj.subcategory and obj.subcategory.category else None
