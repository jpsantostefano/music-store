from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms


def category(request, cat):
    try:
        category = Category.objects.get(name=cat)
        products = Product.objects.filter(category=category)
        return render(request,'category.html',{'products':products,'category':category})
    except:
        messages.success(request, ("That category doesn't exist"))
        return redirect('home')

def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})

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

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out!"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have been register successfuly!"))
            return redirect('home')
        else:
            messages.success(request, ("There is a problem registering. Please try again!"))
            return redirect('register')
    else:
        return render(request, 'account/register.html',{'form':form})

# search bar
def search(request):
    return render(request, 'search.html')

# More
def about(request):
    return render(request, 'more/about.html', {})

def careers(request):
    return render(request, 'more/careers.html', {})

def blog(request):
    return render(request, 'more/blog.html', {})
