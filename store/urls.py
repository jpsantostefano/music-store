from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('profile_view/<int:pk>', views.profile_view, name='profile_view'),
    path('about/', views.about, name='about'),
    path('careers/', views.careers, name='careers'),
    path('blog/', views.blog, name='blog'),
    path('product/<int:pk>', views.product, name='product'),
    path('category/<str:cat>', views.category, name='category'),
    path('search/', views.search, name='search'),
]

