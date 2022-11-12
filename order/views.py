from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from order.models import ShopCart, ShopCartForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from home.models import Setting
from product.models import Category, Product
from user.models import UserProfile
from order.models import OrderForm, Order, OrderProduct
from django.utils.crypto import get_random_string



def index(request):
    return HttpResponse('Order')

@login_required(login_url='/login')  #check user login or not
def addToShopCart(request, id):
    url = request.META.get('HTTP_REFERER') #get the last url0
    current_user = request.user #access user session information

    check_product = ShopCart.objects.filter(product_id= id)
    if check_product:
        control = 1  #the product is in the cart
    else:
        control = 0 #the product is not in the cart
        
    if request.method == 'POST':
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control==1 :  #update shopcart
                data = ShopCart.objects.get(product_id = id)
                data.quantity += form.cleaned_data['quantity']
                data.save()
            else:  #insert to shopcart
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, 'Product added to ShopCart')
        return HttpResponseRedirect(url)
    else: #if there is no post
        if control == 1:
            data = ShopCart.objects.get(product_id = id)
            data.quantity += 1
            data.save()
        else:
            data = ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.save()
        messages.success(request, 'Product added to ShopCart')
        return HttpResponseRedirect(url)
            
        
            
def shopCart(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id = current_user)
    total = 0
    for pro in shopcart:
        total += pro.product.price* pro.quantity
        
    context = {
        'setting' : setting,
        'category' : category,
        'shopcart' : shopcart,
        'total' : total,
    }
    return render(request, 'shopCartProduct.html', context)
    
@login_required(login_url='/login')   
def deleteFromCart(request, id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, 'Your item delete from Shopcart')
    return HttpResponseRedirect('/shopcart')


def orderProduct(request):
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for k in shopcart :
        total += k.product.price * k.quantity
        
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # send credit cart to bank 
            # if the bank responds ok continue, if not show the error
            data = Order()
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper()  #rand code
            data.code = ordercode
            data.save()
            #move Shopcart item to Order Products Item
            shopcart = ShopCart.objects.filter(user_id=current_user.id)
            print('Testing OrderProduct')
            for k in shopcart:
                detail = OrderProduct()
                detail.order_id = data.id # order id
                print(detail.order_id)
                detail.product_id = k.product_id
                print(detail.product_id)
                detail.user_id = current_user.id
                detail.quantity = k.quantity
                detail.price = k.product.price
                detail.amount = k.amount
                detail.save()
                #reduce quantity of sold product from amount of Product
                product = Product.objects.get(id=k.product_id)
                product.amount -= k.quantity
                product.save()
                
            ShopCart.objects.filter(user_id=current_user.id).delete() #clear and delete form Shopcart
            request.session['cart_items'] = 0
            messages.success(request, 'Your order has been completed. Thank You')
            context = {
                'ordercode' : ordercode,
                'category' : category,
            }
            return render(request, 'orderCompleted.html', context)
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/order/orderproduct')
    profile = UserProfile.objects.get(user_id=current_user.id)
    form = OrderForm()
    context = {
        'category' : category,
        'shopcart' : shopcart,
        'total' : total,
        'profile' : profile,
    }
    return render(request, 'orderForm.html', context)