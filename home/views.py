from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Setting, ContactForm, ContactMessage
from django.contrib import messages
from product.models import Category, Product, Images, Comment
from .forms import SearchForm
import json

# Create your views here.
def index(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    product_slider = Product.objects.all().order_by('id')[:3] #first 3 pictures
    # product_latest = Product.objects.all().order_by('-id')[:3] #last 3 pictures
    # product_picked = Product.objects.all().order_by('?')[:3] #random 3 pictures
    
    context = {
        'setting' : setting,
        'page' : 'home',
        'category' : category,
        'product' : product_slider,
    }
    return render(request, 'index.html', context)

def aboutus(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {
        'setting' : setting,
        'category' : category,
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
       
        
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    form = ContactForm
    context = {
        'setting' : setting,
        'form' : form,
        'category' : category
    }
    return render(request, 'contact.html', context)


def category_product(request, id, slug):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    product = Product.objects.filter(category_id=id)
    context = {
        'setting' : setting,
        'category' : category,
        'product' : product,
    }
    return render(request, 'categoryProduct.html', context)
     

def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']
            if catid == 0:
                products = Product.objects.filter(title__icontains=query) #SELECT * FROM product WHERE title LIKE '%query%'
            else:
                products = Product.objects.filter(title__icontains=query, category=catid)
            category = Category.objects.all()
            context = {
                'products' : products,
                'category' : category,  
                'query' : query,  
            }
            return render(request, 'searchProduct.html', context)

    return HttpResponseRedirect('/')   


def searchAuto(request):
    print('testing1')
    
    if request.is_ajax():
        q = request.GET.get('term', '')
        product = Product.objects.filter(title__icontains=q)
        results = []
        for pl in product:
            product_json = {}
            product_json = pl.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def productDetail(request, id, slug):
    
    try:
        product = Product.objects.get(pk=id)
    except Product.DoesNotExist:
        product = None
        
    category = Category.objects.all()
    image = Images.objects.filter(product_id= id)
    comment = Comment.objects.filter(product_id=id, status='True')
    print('tsting')
    for com in comment:
        print(com.create_at) 
        print(type(com.rate))
        for i in range(com.rate):
            print('test')
        
    context = {
        'product' : product,
        'category' : category,
        'image' : image,
        'comment' : comment,
    }
    return render(request, 'productDetail.html', context)
     
     
        
    