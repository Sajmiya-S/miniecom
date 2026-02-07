from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('home',homepage,name='home'),
    path('login',signin,name='login'),
    path('logout',signout,name='logout'),
    path('signup',signup,name='signup'),
    path('profile',profilepage,name='profile'),
    path('editpro/<int:pid>',editprofile,name='editp'),
    path('shopnow',categories,name='catz'),
    path('catwise/<int:cid>',categorywise,name='cwise'),
    path('allp',allproducts,name='shop'),
    path('pro/<pid>',productdetails,name='pdet'),
    path('about',aboutpage,name='about'),
    path('address/',saveaddress,name='addr'),
    path('viewaddr/',viewaddress,name='viewaddr'),
    path('editaddr/<int:aid>/',editaddress,name='editaddr'),
    path('deladdr/<int:aid>/',deleteaddress,name='deladdr'),
    path('add2cart/<int:pid>',addtocart,name='add2cart'),
    path('cart',viewcart,name='cart'),
    path('delcart/<int:id>',deletecartItem,name='remove'),
    path('upcart/<int:id>/<str:op>',updatecartItem,name='update'),
    path('clrcart',clearcart,name='clear'),
    path('orders',vieworders,name='order'),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)