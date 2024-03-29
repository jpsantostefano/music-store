from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Profile, Post, Careers, Subscriber
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django import forms
from .forms import ProfileForm, CareersForm, NewsletterSubscriptionForm
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect



def category(request, cat):
    category = Category.objects.get(name=cat)
    products = Product.objects.filter(category=category)
    return render(request,'category.html',{'products':products,'category':category})

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


def careers(request):
    return render(request, 'more/careers.html', {})


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

# More
# News post
def news(request):
    # Shows all the posts
    posts = Post.objects.all()
    return render(request, 'more/news/news.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'more/news/post_detail.html', {'post': post})

# Careers Contact
def careers(request):
    if request.method == 'POST':
        form = CareersForm(request.POST, request.FILES)
        # Save on database
        if form.is_valid():
            career_instance = form.save()
            # Send email
            subject = 'New careers form'
            message = f"There is a new careers form:\n\nName: {career_instance.full_name}\nPosition: {career_instance.position}\nEmail: {career_instance.email}\nmessage: {career_instance.message}\ncv: {career_instance.cv}"

            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = ['musicstoredublin@gmail.com']  

            send_mail(subject, message, from_email, recipient_list)
            messages.success(request, "Form submitted successfully. Thanks for applying!")
            return redirect('careers')
    else:
        form = CareersForm()

    return render(request, 'more/careers.html', {'form': form})

# About
def about(request):
    return render(request, 'more/about.html', {})

# Newsletter

def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print("Email received:", email)
        if email:
            Subscriber.objects.create(email=email)
            messages.success(request, "Thank you for subscribing!")
            return redirect('home')

    return render(request, 'home.html')