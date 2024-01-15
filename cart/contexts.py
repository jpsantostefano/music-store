from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from store.models import Product


def cart_contents(request):
    bag_items = []
    total = 0
    product_count = 0

    

    context = {
        'bag_items':bag_items,
        'bag_items':total,
        'bag_items':product_count,
    }

    return context