from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Comment
from django.contrib import messages
from .forms import CommentForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .cart import Cart
from django.views.decorators.http import require_POST

def cart_add(request, item_id):
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    if item_id in list(cart.keys()):
        cart[item_id] += quantity
        messages.success(request,
                            (f'Updated {product.name} '
                            f'quantity to {cart[item_id]}'))
    else:
        cart[item_id] = quantity
        messages.success(request, f'Added {product.name} to your cart')
    
    request.session['cart'] = cart
    return redirect(redirect_url)

def cart_summary(request):
	# Get the cart
	cart = Cart(request)
	cart_products = cart.get_products
	quantities = cart.get_quants
	totals = cart.cart_total()
	return render(request, "cart_summary.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals})

@require_POST
def cart_delete(request, item_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=item_id)
    cart.remove(product)
    request.session['session_key'] = cart.cart  # Actualizar manualmente la sesión
    request.session.modified = True  # Marcar la sesión como modificada
    return JsonResponse({'deleted': True})

@require_POST
def cart_update(request, item_id):
   # Obtener los datos del formulario AJAX
    item_id = request.POST.get('item_id')
    new_quantity = request.POST.get('new_quantity')

    # Actualizar la cantidad del artículo en el carrito
    try:
        cart_item = Product.objects.get(id=item_id)
        cart_item.quantity = new_quantity
        cart_item.save()
        data = {'success': True, 'message': 'Quantity updated successfully.'}
    except Product.DoesNotExist:
        data = {'success': False, 'message': 'CartItem does not exist.'}
    except Exception as e:
        data = {'success': False, 'message': str(e)}

    return JsonResponse(data)

# Product       
def product_detail(request,pk):
    product = get_object_or_404(Product, id=pk)
    comments = Comment.objects.filter(product=product)
    # Comment form
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.product = product
            comment.save()
            messages.success(request, "You successfully left a comment!")
            return redirect('product_detail', pk=product.id)
    else:
        comment_form = CommentForm()

    return render(request, 'product_detail.html', {'product': product, 'comments': comments, 'comment_form': comment_form, 'pk':pk})

# Comment
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        if request.POST.get('confirm_delete'):
            comment.delete()
            messages.success(request, "You successfully deleted your comment!")
            return redirect('product', pk=comment.product.id)
    return render(request, 'reviews/delete_comment.html', {'comment': comment})


def edit_comment(request, comment_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, id=comment_id)
        # Edit comment form
        if request.method == 'POST':
            form = CommentForm(request.POST, request.FILES, instance=comment)
            if form.is_valid():
                form.save()
                messages.success(request, "You successfully edited your comment!")
                return redirect('product', pk=comment.product.id)
        else:
            form = CommentForm(instance=comment)
        return render(request, 'reviews/edit_comment.html', {'form': form, 'comment': comment})
    else:
        messages.error(request, "You must be logged in to see this page.")
        return redirect('home')

