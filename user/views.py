from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from product.models import Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth.decorators import login_required


# Create your views here.

from home.models import Setting, ContactForm, ContactMessage

@login_required(login_url='/login') # Check login
def index(request):
    return HttpResponse('User')

def loginForm(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user )
            current_user = request.user
            # print(f'testing {current_user.id}')
            userprofile = UserProfile.objects.get(user_id=current_user.id)
            print(f'testing {userprofile.image.url}')
            request.session['userimage'] = userprofile.image.url
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, 'Login Failed  ! Username or Password incorrect')
    category = Category.objects.all()
    context = {
       'category' : category
    }
    return render(request, 'loginForm.html', context)

def signunForm(request):
    category = Category.objects.all()
    context = {
        'category': category,
    }
    return render(request, 'loginForm.html', context)

def logoutFun(request):
    logout(request)
    return HttpResponseRedirect('/')
