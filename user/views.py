from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from product.models import Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from django.contrib.auth.models import User

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
