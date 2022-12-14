from django.urls import path
from . import views


urlpatterns = [
    path('<id>/',views.wishlist,name='wishlist'),
    path('show',views.wis_show,name='show'),

] 