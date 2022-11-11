from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addToShopCart/<int:id>', views.addToShopCart, name='addToShopCart'),
    path('deletefromcart/<int:id>', views.deleteFromCart, name='deleteFromCart'),
]
