from django.db import models
from django.contrib.auth.models import User
from store.models import Product

# Create your models here.

# Comment

# Reviews
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.product.name}'

    class Meta:
        ordering = ['date_added']


class CartManager(models.Manager):
    def get_or_create_cart(self, user):
        cart, created = self.get_or_create(user=user)
        return cart

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Otros campos del carrito
    objects = CartManager()
    def calculate_total(self):
        # Lógica para calcular el total del carrito
        pass
