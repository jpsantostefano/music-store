from django.urls import path
from . import views

urlpatterns = [
    path('product/<int:pk>', views.product_detail, name='product_detail'),
    path('cart_summary', views.cart_summary, name='cart_summary'),
    path('add/<item_id>/', views.cart_add, name='cart_add'),
    #path('delete/', views.cart_delete, name='cart_delete'),
    #path('update/', views.cart_update, name='cart_update'),
    # Comments
    path('delete_comment/<int:pk>', views.delete_comment,name='delete_comment'),
    path('edit_comment/<int:pk>', views.edit_comment,name='edit_comment'),
    
]