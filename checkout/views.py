from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm

def checkout(request):
    cart = request.session.get('cart', {})
    

    order_form = OrderForm()
    template = 'checkout.html'
    context = {
        'order_form': order_form,
    }

    return render(request, template, context)