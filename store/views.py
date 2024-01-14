from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Profile, Comment
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms
from .forms import ProfileForm, CommentForm


def category(request, cat):
    try:
        category = Category.objects.get(name=cat)
        products = Product.objects.filter(category=category)
        return render(request,'category.html',{'products':products,'category':category})
    except:
        messages.success(request, ("That category doesn't exist"))
        return redirect('home')

def product(request,pk):
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
            return redirect('product', pk=product.id)
    else:
        comment_form = CommentForm()

    return render(request, 'product.html', {'product': product, 'comments': comments, 'comment_form': comment_form, 'pk':pk})




def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})

# Account
def sign_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have been logged in!"))
            return redirect('home')
        else:
            messages.success(request, ("There was an error, please try again"))
            return redirect('sign_in')
    else:
        return render(request, 'account/sign_in.html', {})


def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password != password2:
            message.alert(request, "You're typing a different password.")
            return redirect('register')
        # Saves the user information
        myuser = User.objects.create_user(username=username, password=password)
        myuser.save()
        user = authenticate(username=username, password=password)
        login(request, user)
        messages.success(request, "Your Account has been successfully created.")
        return redirect('home')
    return render(request, 'account/register.html')

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out!"))
    return redirect('home')

# Search bar
def search(request):
    return render(request, 'search.html')

# More
def about(request):
    return render(request, 'more/about.html', {})

def careers(request):
    return render(request, 'more/careers.html', {})

def blog(request):
    return render(request, 'more/blog.html', {})

# Profile views:
def profile_view(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        return render(request, 'account/profile_view.html', {'profile': profile})
    else:
        return redirect('home')


def edit_profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        print(profile)
        # Verify if the user is the ownwer of the profile
        if request.user == profile.user:
            if request.method == 'POST':
                # Process data
                form = ProfileForm(request.POST, request.FILES, instance=profile)
                if form.is_valid():
                    form.save()
                    messages.success(request, "You successfully edited your profile!")
                    return redirect('profile_view', pk=pk)
            else:
                # If it's a GET request, shows the edition form.
                form = ProfileForm(instance=profile)
            return render(request, 'account/edit_profile.html', {'form': form})
        else:
            # If the user is not permited to see this page.
            messages.error(request, "You don't have permission to edit this profile.")
            return redirect('home')
    else:
        messages.error(request, "You must be logged in to see this page.")
        return redirect('home')

# Comment
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        if request.POST.get('confirm_delete'):
            comment.delete()
            messages.success(request, "You successfully deleted your comment!")
            return redirect('product', id=comment.product.id)
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