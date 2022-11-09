from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Setting, ContactForm, ContactMessage
from django.contrib import messages
from product.models import Category, Product

# Create your views here.
def index(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    product_slider = Product.objects.all().order_by('id')[:3] #first 3 pictures
    product_latest = Product.objects.all().order_by('-id')[:3] #last 3 pictures
    product_picked = Product.objects.all().order_by('?')[:3] #random 3 pictures
    
    context = {
        'setting' : setting,
        'page' : 'home',
        'category' : category,
        'product' : product_slider,
    }
    print("Testing: ", category)
    
    return render(request, 'index.html', context)

def aboutus(request):
    setting = Setting.objects.get(pk=1)
    context = {
        'setting' : setting
    }
    return render(request, 'about.html', context)

def contactus(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage() #create relation with model 
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  #save data to table
            messages.success(request, 'You message have been sent. Thank for your message')
            return HttpResponseRedirect('/contact')
        
        
    setting = Setting.objects.get(pk=1)
    form = ContactForm
    context = {
        'setting' : setting,
        'form' : form
    }
    return render(request, 'contact.html', context)


def category_product(request, id, slug):
    products = Product.objects.filter(category_id=id)
    return HttpResponse(products)