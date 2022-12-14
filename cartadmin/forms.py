from category.models import Category
from store.models import Product
from django import forms


class AddProductCategory(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category_name','slug','description','cat_image')



class AddNewProduct(forms.ModelForm):
    images = forms.ImageField(label=('images'),required=False)
    class Meta:
        model = Product
        fields = ('product_name' ,'slug','description','price','images','stock','is_available','category',)

        