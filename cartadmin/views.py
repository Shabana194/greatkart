from django.shortcuts import render,redirect
from accounts.models import Account
from store.models import Product,Category
from orders.models import Payment
from orders.forms import PaymentForm
from django.http import JsonResponse
from .forms import AddProductCategory,AddNewProduct
from orders.models import Order,Payment
from django.contrib import auth,messages
from django.contrib.auth.decorators import login_required

# cartadmin start

def cartadmin_dashboard(request):
    chartlist = list()
    total_order = len(Order.objects.all())
    paypal_total = len(Payment.objects.filter(payment_method = "PAYPAL"))
    cash_on_total = len(Payment.objects.filter(payment_method = "CASH ON DELIVERY"))
    print(f"total order {total_order} paypal total {paypal_total} cashon delivery {cash_on_total}")
    chartlist.append(total_order)
    chartlist.append(paypal_total)
    chartlist.append(cash_on_total)
    return render(request,'cartadmin/baseadmin.html',{'chartlist':chartlist})

@login_required(login_url='admin_login')
def admin_logout(request):
    auth.logout(request)
    messages.success(request,'You are logged out')
    return redirect('admin_login')


def admin_login(request):
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']
        user=auth.authenticate(email=email,password=password)
        if user is not None:
            if user.is_admin:
                return redirect('cartadmin_dashbord')
            return redirect('admin_login')
    return render(request,'accounts/adminlogin.html')


# users start

def user_details(request):
    user_list = Account.objects.all()
    return render(request,'cartadmin/userdetails.html',{'user_list':user_list})

def admin_sales_report(request):
    return render(request,'cartadmin/salesreport.html')




def block_user(request):
    id = request.GET['id']
    print(id)
    a = Account()
    account = Account.objects.get(id = id)
    print(account.is_active)
    account.is_active = 0
    account.save()
    return JsonResponse({'result':True})





def unblock_user(request):
    id = request.GET['id']
    print(id)
    a = Account()
    account = Account.objects.get(id = id)
    print(account.is_active)
    account.is_active = 1
    account.save()
    return JsonResponse({'result':True})




# product start

def display_product(request):
    product_list = Product.objects.all()
    return render(request,'cartadmin/displayproduct.html',{'product_list':product_list})



def add_product(request):
    forms = AddNewProduct(request.POST or None)
    if request.method == 'POST':
        if forms.is_valid():
            pro = Product()
            pro.product_name = request.POST['product_name']
            pro.slug = request.POST['slug']
            pro.description = request.POST['description']
            pro.price = request.POST['price']
            pro.images = request.FILES['images']
            pro.stock = request.POST['stock']
            pro.is_available = 1
            pro.category_id = request.POST['category']
            pro.save()
            return redirect('display_product')
    return render(request,'cartadmin/addproduct.html',{'forms':forms})




def edit_product(request,id):
    p = Product.objects.get(id = id)
    '''
    AddNewProduct class is use for edit previous datas but the fields is same 
    so use same class for different functionality
    '''
    forms = AddNewProduct(request.POST or None,instance=p)
    if request.method == 'POST':
        pro = Product()
        pro.product_name = request.POST['product_name']
        pro.slug = request.POST['slug']
        pro.description = request.POST['description']
        pro.price = request.POST['price']
        pro.stock = request.POST['stock']
        print(request.POST['is_available'])
        pro.is_available = 1
        pro.category_id = request.POST['category']
        try:
            pro.images = request.FILES['images']
        except:
            forms.save()
            return redirect('display_product')
        else:
            pro.save()
            return redirect('display_product')
    return render(request,'cartadmin/editproduct.html',{'forms':forms})




def delete_product(request):
    print('delete')
    id = request.GET['id']
    Product.objects.get(id=id).delete()
    return JsonResponse({'result':True})



# category start 

def product_category(request):
    category_list = Category.objects.all()
    return render(request,'cartadmin/category.html',{'category_list':category_list})



def add_product_category(request):
    forms = AddProductCategory(request.POST or None)
    if request.method == 'POST':
        if forms.is_valid():
            cat = Category()
            cat.category_name = request.POST['category_name']
            cat.slug = request.POST['slug']
            cat.description = request.POST['description']
            cat.cat_image = request.FILES['cat_image']
            cat.save()
            return redirect('product_category')
        else:
            print(True)
    return render(request,'cartadmin/addcategory.html',{'forms':forms})



def order_history(request):
    orders = Order.objects.all()
    return render(request,'cartadmin/orderhistory.html',{'orders':orders})