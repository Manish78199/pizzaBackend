from pizzaapp import views
from django.urls import path

urlpatterns = [
    path('api/getallproduct', views.allprod,name="allprod"),
    path('api/auth/user', views.myuser,name="allprod"),
    path('api/auth/user/login', views.userlogin,name="allprod"),
    path('api/auth/mycart', views.mycart,name="mycart"),
    path('api/auth/vendor/login', views.vendorLogin,name="vendorLogin"),
    path('api/auth/vendor/product', views.vendor,name="vendor"),
    # path('api/mycart', views.index,name="home"),
    path('api/product/<int:id>', views.prod,name="home"),
    path("api/auth/transaction/createorder",views.OrderApi,name="order api"),
    path("api/auth/transaction/verifySignature", views.verifySignature ,name="order api"),
    path('', views.index,name="home"),
    path('', views.index,name="home"),
    path('', views.index,name="home"),
    path('', views.index,name="home"),
    path('', views.index,name="home"),
    path('', views.index,name="home"),
]