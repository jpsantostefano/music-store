from .cart import Cart

# Create context processor. The cart can work on all pages
def cart(request):
    # Return the default data from our Cart
    return {'cart': Cart(request)}