from django.shortcuts import render,redirect
from store.models import Variation,Product
from .models import WishlistItem
from django.http import HttpResponse
# Create your views here.

def wis_show(request):
    return render(request,'store/wishlist.html')
    
def wishlist(request,id):
    if request.method == 'POST':
        for list in request.POST:
            pass
        color = request.POST['color']
        size = request.POST['size']
        product = Product.objects.get(id=id)
        variation = Variation.objects.get(product=product, variation_category__iexact='color', variation_value__iexact=color)
        if request.user.is_authenticated:
            wishlist_item = WishlistItem.objects.create(
                product=product,
                user=request.user,
                quantity=0,
            )
            wishlist_item.save()
            return redirect('show')