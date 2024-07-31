from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.Home, name='Home'),
    path('login/', views.Login, name='Login'),
    path('signup/', views.Signup, name='Sign Up'),
    path('logout/', views.Logout, name='Logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('resend_activation_email/', views.resend_activation_email, name='resend_activation_email'),
    path('add_product/', views.Add_Product, name='Add_Product'),
    path('account/', views.Account, name='Account'),
    path('password_reset/', views.password_reset_request, name='password_reset_request'),
    path('password_reset_confirm/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('about/', views.About, name='About'),
    path('contact/', views.Contact, name='Contact'),
    path('products/<int:pk>/', views.Products, name='product'),
    path('add_to_cart/<int:pk>/', views.Add_To_Cart, name='Add_To_Cart'),
    path('cart/', views.Cart, name='Cart'),
    path('remove_item/<int:pk>/', views.Remove_Item, name='Remove_item'),
    path('checkout/<int:order_id>/', views.Checkout, name='Checkout'),
    path('orders/', views.Orders, name='Orders'),
    path('orderdetails/<int:pk>/', views.OrderDetails, name='OrderDetails'),
    path('myorders/', views.MyOrders, name='MyOrders'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.USERP_MEDIA_URL, document_root=settings.USERP_MEDIA_ROOT)