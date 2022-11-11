from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from order.models import ShopCart, ShopCartForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from home.models import Setting
from product.models import Category



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
    
    
def deleteFromCart(request, id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, 'Your item delete from Shopcart')
    return HttpResponseRedirect('/shopcart')