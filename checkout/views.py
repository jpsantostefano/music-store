from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm

def checkout(request):
    cart = request.session.get('cart', {})
    

    order_form = OrderForm()
    template = 'checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51OXAtRAAWBwzcB04e0eXGyoSYRAJtQ33isWD1qychE5eMOcAQvkmqIgxkUA79GF29DyeJItSGvnR8v5cRxdBFhsX00lJB94eHk',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)