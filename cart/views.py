from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Comment
from django.contrib import messages
from .forms import CommentForm


def cart_summary(request):
    return render(request, 'cart_summary.html')

def cart_add(request, item_id):
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    if item_id in list(cart.keys()):
        cart[item_id] += quantity
    else:
        cart[item_id] = quantity
    
    request.session['cart'] = cart
    return redirect(redirect_url)

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