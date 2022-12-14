from django.db import models

# Create your models here.
from django.db import models
from store.models import Product,Variation
from accounts.models import Account

# Create your models here.
class Wishlist(models.Model):
    wishlist_id=models.CharField(max_length=255,blank=True)
    date_added=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.wishlist_id

class WishlistItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    variations=models.ManyToManyField(Variation,blank=True)
    wishlist=models.ForeignKey(Wishlist,on_delete=models.CASCADE,null=True)
    quantity=models.IntegerField()
    is_active=models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __unicode__(self):
        return self.product