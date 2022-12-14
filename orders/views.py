from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from carts.models import CartItem
from .models import Order, Payment, OrderProduct,Coupon
from .forms import OrderForm,PaymentForm
import datetime
from accounts.models import Account
import json
import razorpay
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from accounts import otphelper



def cash_on_delivery(request):
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=otphelper.order_number)
    payment_update = Payment(
        user = request.user,
        payment_id = 'Not Applicable' ,
        payment_method = otphelper.payment_method,
        amount_paid = otphelper.amount_of_pay,
        status = "Pending"
    )
    payment_update.save()

    order.payment = payment_update
    order.is_ordered = True
    order.save()

    #Move the cart items to the orderproduct table
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment_update
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()

        #Reduce the quantity of sold products
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    CartItem.objects.filter(user=request.user).delete()

    ordered_products = OrderProduct.objects.filter(order_id=order.id)

    subtotal = 0
    for i in ordered_products:
            subtotal += i.product_price * i.quantity


    context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'subtotal': subtotal,
            'payment_update':payment_update,
            'total':otphelper.total,
        }

    return render(request, 'orders/order_complete.html', context)

 



def payments(request):
    body=json.loads(request.body)
    print(body)
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

    # Store transaction details inside Payment model
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )

    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()
    #Move the cart items to the orderproduct table
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()

    #Reduce the quantity of sold products
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    #Clear cart
    CartItem.objects.filter(user=request.user).delete()

    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)


     
def place_order(request,total=0,quantity=0):
    current_user = request.user
    # If the cart count is less than or equal to 0, then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = otphelper.amount_of_pay = total + tax
    if request.method == 'POST':
        form = OrderForm(request.POST)
        
        if form.is_valid():
            # Store all the billing information inside Order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20210305
            order_number = current_date + str(data.id)#concatenating order id with current_date
            data.order_number = otphelper.order_number = order_number
            data.payment_option = otphelper.payment_method = form.cleaned_data['payment_option']
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            

            print(order.full_address)
            coupon = Coupon.objects.all()
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
                'payment_option':data.payment_option,
                'coupon':coupon,
            
            }
            if data.payment_option == 'CASH ON DELIVERY':

                return render(request,'orders/cashondelivery.html',context)


            elif data.payment_option == 'PAYPAL':

                return render(request,'orders/payments.html',context)



        else:
            return redirect('checkout')
    

def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        payment = Payment.objects.get(payment_id=transID)

        coupon = Coupon.objects.all()
        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
            'coupon':coupon
        }
        return render(request, 'orders/order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')


def apply_coupon(request):
    off = request.GET['off']
    id = request.GET['id']
    coupon  = Coupon.objects.get(id=id)
    coupon.is_use = True
    coupon.save()
    total = otphelper.amount_of_pay
    total = otphelper.amount_of_pay * (100-int(off))/100
    otphelper.total = total
    return JsonResponse({'total':total})

