from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from product.models import Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from order.models import Order, OrderProduct
from product.models import Comment

# Create your views here.

from home.models import Setting, ContactForm, ContactMessage

@login_required(login_url='/login') # Check login
def index(request):
    category = Category.objects.all()
    current_user = request.user
    userprofile = UserProfile.objects.get(user_id=current_user.id)
    context = {
        'category' : category,
        'profile' : userprofile,
    }
    return render(request, 'userProfile.html', context)

def loginForm(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user )
            current_user = request.user
            userprofile = UserProfile.objects.get(user_id=current_user.id)
            request.session['userimage'] = userprofile.image.url
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, 'Login Failed  ! Username or Password incorrect')
    category = Category.objects.all()
    context = {
       'category' : category
    }
    return render(request, 'loginForm.html', context)

def signupForm(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            #create data in profile table for user
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = 'images/uesrs/user.png'
            data.save()
            messages.success(request, 'Your account has been created successfully')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/signup')
            
    
    form = SignUpForm()
    category = Category.objects.all()
    context = {
        'category': category,
        'form': form,
        
    }
    return render(request, 'signupForm.html', context)

def logoutFun(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url='/login') # Check login
def userUpdate(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user) #request.user is user data
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated')
            return HttpResponseRedirect('/user')
        
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.userprofile)  #userprofile model -> onetoone field relation with user
        category = Category.objects.all()
        context = {
            'category' : category,
            'user_form' : user_form,
            'profile_form' : profile_form,
            
        }
        return render(request, 'userUpdate.html', context)
        
    return HttpResponseRedirect('Userupdate')



@login_required(login_url='/login') # Check login
def userPassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) #important
            messages.success(request, 'Your password was successfully changed')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Please correct the error below <br>'+str(form.errors))
            return HttpResponseRedirect('/user/password')

    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user, request.POST)
        context = {
            'form': form,
            'category' : category,
        }
        return render(request, 'userPassword.html', context)
    
    
def userOrder(request):
    category = Category.objects.all()
    current_user =request.user
    orders = Order.objects.filter(user_id=current_user.id)
    
    context = {
        'category' : category,
        'orders' : orders,
    }
    return render(request, 'userOrder.html', context)



@login_required(login_url='/login') # Check login
def userOrderDetail(request, id):
    category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)
    orderitem = OrderProduct.objects.filter(order_id = id)
    print('Testing country', order.country)
        
    context ={
        'category' : category,
        'order' : order,
        'orderitem' : orderitem,
    }
    return render(request, 'userOrderDetail.html', context)

@login_required(login_url='/login') # Check login
def userOrderProduct(request):
    category = Category.objects.all()
    current_user = request.user
    orderitem = OrderProduct.objects.filter(user_id=current_user.id)
    
    context ={
        'category' : category,
        'orderitem' : orderitem,
    }
    return render(request, 'userOrderProduct.html', context)


@login_required(login_url='/login') # Check login
def userOrderProductDetail(request, id, oid):
    category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=oid)
    orderitem = OrderProduct.objects.filter(user_id=current_user.id, id=id)
    
    context ={
        'category' : category,
        'order' : order,
        'orderitem' : orderitem,
    }
    return render(request, 'userOrderProductDetail.html', context)

    
def userComment(request):
    category = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    
    context ={
        'category' : category,
        'comments' : comments,
    }
    return render(request, 'userComment.html', context)


def userDeleteComment(request, id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Comment deleted')
    return HttpResponseRedirect('/user/comment')