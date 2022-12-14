from django.urls import path
from . import views


urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('otp<otp>/',views.otp_validate,name='otp_validate'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('',views.dashboard,name='dashboard'),
    path('forgotPassword',views.forgotPassword,name='forgotPassword'),
    #path('adminlogin/',views.admin_login,name='admin_login'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),

    
]
