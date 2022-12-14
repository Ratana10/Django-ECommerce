"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from home import views
from order import views  as orderViews
from user import views  as userViews
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('home.urls')),
    path('home/', include('home.urls')),
    path('product/', include('product.urls')),
    path('order/', include('order.urls')),
    path('user/', include('user.urls')),
    path('about/', views.aboutus, name='about'),
    path('contact/', views.contactus, name='contact'),
    path('category/<int:id>/<slug:slug>', views.category_product, name='category'),
    path('search/', views.search, name='searchProduct'),
    path('searchAuto/', views.searchAuto, name='searchAuto'),
    path('product/<int:id>/<slug:slug>', views.productDetail, name='productDetail'),
    path('shopcart/', orderViews.shopCart, name='shopCart'),
    path('login/', userViews.loginForm, name='login'),
    path('logout/', userViews.logoutFun, name='logout'),
    path('signup/', userViews.signupForm, name='signup'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




    