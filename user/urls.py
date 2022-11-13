from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('update/', views.userUpdate, name='update'),
    path('password/', views.userPassword, name='password'),
    path('order/', views.userOrder, name='order'),
    path('orderdetail/<int:id>', views.userOrderDetail, name='orderDetail'),
    path('orderproduct/', views.userOrderProduct, name='orderProduct'),
    path('orderproductdetail/<int:id>/<int:oid>', views.userOrderProductDetail, name='orderProductDetail'),
    path('comment/', views.userComment, name='comment'),
    path('deletecomment/<int:id>', views.userDeleteComment, name='deleteComment'),
]
