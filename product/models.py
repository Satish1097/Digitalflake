from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image=models.ImageField(upload_to="images/category_image/")
    is_active=models.BooleanField(default=True)


    def __str__(self):
        return self.name


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    name = models.CharField(max_length=255, unique=True)
    image=models.ImageField(upload_to="images/subcategory_image/")
    is_active=models.BooleanField(default=True)


    def __str__(self):
        return f"{self.category.name} - {self.name}"


class Product(models.Model):
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=255)
    image=models.ImageField(upload_to="images/product_image/")
    is_active=models.BooleanField(default=True)


    def __str__(self):
        return f"{self.name} ({self.subcategory.name})"
