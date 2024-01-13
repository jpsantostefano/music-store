from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms
from .forms import ProfileForm


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

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out!"))
    return redirect('home')

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
        messages.success(request, "Your Account has been successfully created.")
        return redirect('home')
    return render(request, 'account/register.html')

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