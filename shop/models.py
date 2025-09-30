from django.db import models
from author.models import AuthorProfile
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    photo = models.ImageField(upload_to='products_category')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    details = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(AuthorProfile, on_delete=models.CASCADE)
    is_draft = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    inventory = models.IntegerField(default=1)

    def __str__(self):
        return self.name


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.product.name}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_user_product_wishlist')
        ]
