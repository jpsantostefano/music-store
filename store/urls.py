from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    # Profile
    path('sign_in/', views.sign_in, name='sign_in'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('profile_view/<int:pk>', views.profile_view, name='profile_view'),
    path('edit_profile/<int:pk>', views.edit_profile, name='edit_profile'),
    # More
    path('about/', views.about, name='about'),
    path('careers/', views.careers, name='careers'),
    path('blog/', views.blog, name='blog'),
    # Product
    
    path('product/<int:pk>', views.product, name='product'),
    path('category/<str:cat>', views.category, name='category'),
    path('search/', views.search, name='search'),
    # Comments
    path('delete_comment/<int:comment_id>', views.delete_comment,name='delete_comment'),
    path('edit_comment/<int:comment_id>', views.edit_comment,name='edit_comment'),
    # Post
    path('<slug:slug>/', views.post_detail, name='post_detail'),
]

