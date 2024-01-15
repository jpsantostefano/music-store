from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import timezone
from datetime import datetime

def current_date():
    return datetime.today().isoformat()

# Categories of Products
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    # Chagnes the name Categorys for categories on admin panel
    class Meta:
        verbose_name_plural = 'categories'

# Customers
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    image = models.ImageField(null=True, blank=True, upload_to='media/')

    def __str__(self):
        return self.user.username


# Create Profile when a new user signs up
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()


post_save.connect(create_profile, sender=User)

# All the products
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product/')

    def __str__(self):
        return self.name




# Post
class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    date = models.DateField(default=current_date)
    body = models.TextField()
    image = models.ImageField(null=True, blank=True, upload_to='images/')

    def __self__(self):
        return self.title

