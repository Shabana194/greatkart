from django.urls import path
from .views import *


urlpatterns = [
    path('login',admin_login,name='admin_login'),
    path('dashboard',cartadmin_dashboard,name='cartadmin_dashbord'),
    path('details/',user_details,name='user_details'),
    path('block/',block_user,name='block_user'),
    path('unblock/',unblock_user,name='unblock_user'),
    path('category/',product_category,name='product_category'),
    path('addcategory/',add_product_category,name='add_product_category'),
    path('product/',display_product,name='display_product'),
    path('addnewproduct/',add_product,name='add_product'),
    path('edit<id>/',edit_product,name='edit_product'),
    path('delete',delete_product,name='delete_product'),
    path('history/',order_history,name='order_history'),
    path('logout/',admin_logout,name='admin_logout'),
    
    
]
