from django.shortcuts import get_object_or_404,render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import login , authenticate ,logout
from django.contrib import messages
from YLO.forms import *
from YLO.models import *
from django.contrib.auth.decorators import user_passes_test,  login_required
from django.db.models import Q

from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from YLO.token import *  
from django.core.mail import EmailMessage 
from django.contrib.auth import get_user_model
from django.http import HttpResponse , HttpResponseRedirect 
from django.urls import reverse
from django.core.mail import send_mail

from random import shuffle

from django.utils import timezone

# Create your views here.

def Home(request):   
    products = Product.objects.all()
    return render(request, 'Home.html' , {'products':products})

 
def Login(request):
    if request.user.is_authenticated:
        return redirect('Home')

    if request.method == 'POST':
        email_or_username = request.POST.get('Email')
        password = request.POST.get('Password')
        
        if '@' in email_or_username:
            users = User.objects.filter(email=email_or_username)
        else:
            users = User.objects.filter(username=email_or_username)
        
        user = users.filter(Q(username=email_or_username) | Q(email=email_or_username)).first()
        
        if user is not None:
            if user.is_active:
                auth_user = authenticate(request, username=user.username, password=password)
                if auth_user is not None:
                    login(request, auth_user)
                    messages.success(request, 'Login successful. Welcome!')
                    return redirect('Home')
                else:
                    messages.error(request, 'Invalid credentials')
            else:
                resend_activation_url = reverse('resend_activation_email')
                activation_message = f"""Your account is not active. Please check your email to activate your account or 
                <a href="{resend_activation_url}">Resend activation email</a>."""
                messages.error(request, activation_message, extra_tags='safe')
        else:
            messages.error(request, 'User does not exist or Invalid credentials')
            
    return render(request, 'Assets/Login.html')

def Signup(request):

    if request.user.is_authenticated:
        return redirect('Home')

    if request.method == 'POST':
        username = request.POST.get('user_name')
        email = request.POST.get('Email')
        password1 = request.POST.get('Password1')
        password2 = request.POST.get('Password2')
        otp = request.POST.get('otp')
        contact = request.POST.get('Contact')

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.is_active = False
                user.save()
                data = Customer(user=user,contact=contact)
                data.save()

                current_site = get_current_site(request)
                mail_subject = 'Activate your account'
                message = render_to_string('Assets/activeemail.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = email  
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()

                messages.success(request, 'Account created successfully. Please check your email to activate your account.')
                return redirect('Login')
        else:
            messages.error(request, 'Passwords do not match')

    return render(request, 'Assets/Signup.html')

def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
    else:  
        return HttpResponse('Activation link is invalid!')  

def resend_activation_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            if user.is_active:
                messages.info(request, 'Your account is already active.')
            else:
                current_site = get_current_site(request)
                mail_subject = 'Activate your account'
                message = render_to_string('Assets/activeemail.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = email  
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                messages.success(request, 'Activation email has been resent. Please check your email.')
                return redirect('Login')
        except User.DoesNotExist:
            messages.error(request, 'Account with this email does not exist.')

    return render(request,'Assets/resendemail.html')

def Logout(request):
    logout(request)
    messages.success(request, 'Logout successfully')
    return redirect('Home')

@user_passes_test(lambda u: u.is_superuser)
def Add_Product(request):

    if request.method == 'POST':

        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product Added successfully')
            return redirect('Home')
        else:
            messages.error(request, 'Some Error Occurred')

    else:

        form = ProductForm()

    return render(request,'Assets/AddProduct.html',{'form':form})

@login_required
def Account(request):

    user_form = UserForm(instance=request.user)
    customer = request.user.customer

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        
        if user_form.is_valid() and form.is_valid():  

            form.clean_password()
            user_form.save()
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('Account')
    
        else:
            messages.error(request, 'Form submission failed due to incorrect password, format, or size.')

    else:
        form = CustomerForm(instance=customer)

    return render(request, 'Assets/Account.html', {'user_form': user_form, 'form': form, 'customer': customer})


def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    c = {
                        "email": user.email,
                        "domain": request.META["HTTP_HOST"],
                        "site_name": "YourSite",
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": account_activation_token.make_token(user),
                        "protocol": "http",
                    }
                    email_template_name = "Assets/password_reset_email.html"
                    email = render_to_string(email_template_name, c)
                    send_mail("Password reset request", email, "admin@example.com", [user.email], fail_silently=False)
                messages.success(request, 'An email has been sent to reset your password.')
                return HttpResponseRedirect(reverse('Login'))
            else:
                messages.error(request, 'No user found with that email address.')
    else:
        form = PasswordResetRequestForm()
    return render(request, "Assets/password_reset.html", {"form": form})

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == "POST":
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            if new_password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return render(request=request, template_name="Assets/password_reset_confirm.html")
            
            user.set_password(new_password)
            user.save()
            
            messages.success(request, 'Your password has been reset successfully. You may now log in.')
            return HttpResponseRedirect(reverse('Login'))
        
        return render(request=request, template_name="Assets/password_reset_confirm.html", context={'uidb64': uidb64, 'token': token})
    else:
        messages.error(request, 'The password reset link is invalid or has expired.')
        return HttpResponseRedirect(reverse('Login'))


def About(request):
    return render(request , 'Assets/About.html')

def Contact(request):
    return render(request , 'Assets/Contact.html')

def Products(request,pk):
    product = Product.objects.get(pk=pk)
    products = Product.objects.all()
    shuffled_products = list(products) 
    shuffle(shuffled_products)
    if product.Sizes:
        sizes_list = product.Sizes.split(',')
    else:
        sizes_list = []
    return render(request , 'Assets/product.html',{'product':product,'s_products':shuffled_products,'products': products,'sizes_list': sizes_list})

@login_required 
def Add_To_Cart(request,pk):
    product = Product.objects.get(pk=pk)
    size = None

    if request.method == 'POST':
        size = request.POST.get('size')
        if not size:
            messages.error(request, "Please select a size.")
            return redirect('product', pk=pk)

    Order_Item, created = OrderItem.objects.get_or_create(
        Product = product,
        user = request.user,
        Ordered = False,
        size=size
    )

    Order_QS = Order.objects.filter(user=request.user,Ordered=False)
    if Order_QS.exists():
        order = Order_QS[0]
        if order.Items.filter(Product__pk = pk,size=size).exists():
            if product.Stock == 1:
                messages.info(request,"Product is out of Stock")
                return redirect("product",pk=pk)
            else: 
                Order_Item.Quantity += 1
                Order_Item.save()
                messages.info(request,"Product added to cart successfully!")
                return redirect("Cart")
        else:
            order.Items.add(Order_Item)
            messages.info(request,"Product added to cart successfully!")
            return redirect("product",pk=pk)
    else: 
        Ordered_Date = timezone.now()
        order = Order.objects.create(user=request.user,Ordered_Date= Ordered_Date)
        order.Items.add(Order_Item)
        messages.info(request,"Product added to cart successfully!")
        return redirect("product",pk=pk)

def Cart(request):
    if Order.objects.filter(user=request.user,Ordered=False).exists():
        order = Order.objects.get(user = request.user,Ordered=False)
        return render(request, 'Assets/Cart.html',{'order':order})
    return render(request, 'Assets/Cart.html',{'message':"Your Cart Is Empty"})

def Remove_Item(request, pk):
    order_qs = Order.objects.filter(user=request.user, Ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.Items.filter(Product__pk=pk).exists():
            order_item = order.Items.filter(Product__pk=pk, user=request.user, Ordered=False).first()

            if order_item.Quantity > 1:
                order_item.Quantity -= 1
                order_item.save()
            else:
                order_item.delete()
                messages.info(request, "Item removed from your cart")
            return redirect("Cart")
        else:
            messages.info(request, "This item is not in your cart")
            return redirect("Cart")
    else:
        messages.info(request, "You don't have any active order")
        return redirect("Cart")


@login_required
def Checkout(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    customer = request.user.customer

    if (not customer.gender or
        not customer.contact or
        not customer.state or
        not customer.city or
        not customer.pincode or
        not customer.address or
        not request.user.first_name or
        not request.user.last_name):
        
        messages.error(request, "Please complete your profile before checking out.")
        return redirect('Account')

    order.Ordered = True
    order.save()

    for order_item in order.Items.all():
        order_item.Ordered = True
        order_item.save()
        messages.success(request, "Your order has been placed successfully. Please wait for the confirmation email.")

    return redirect('Orders')

    
@user_passes_test(lambda u: u.is_superuser)
def Orders(request):
    orders = Order.objects.filter(Items__Ordered=True).distinct()

    order_data = []

    for order in orders:
        user = order.user 
        ordered_items = order.Items.filter(Ordered=True)

        order_info = {
            'order_id': order.id,
            'user_name': user.username,
            'user_email': user.email,
            'products': [],
        }

        for item in ordered_items:
            product_info = {
                'name': item.Product.Product_Name,
                'price': item.Product.Price,
                'size': item.size,
                'image': item.Product.Product_Image.url,
                'quantity': item.Quantity,
                'Order_Delivered': item.Order_Delivered,
            }
            order_info['products'].append(product_info)

        order_data.append(order_info)

    context = {
        'order_data': order_data,
    }

    return render(request, 'Assets/Orders.html', context)


def OrderDetails(request,pk):
    order = get_object_or_404(Order, id=pk)
    user = order.user
    customer = Customer.objects.get(user=user)
    ordered_items = order.Items.filter(Ordered=True)

    product_details = []

    for item in ordered_items:
        product_detail = {
            'product_name': item.Product.Product_Name,
            'price': item.Product.Price,
            'size': item.size,
            'image': item.Product.Product_Image.url,
            'quantity': item.Quantity,
        }
        product_details.append(product_detail)

    context = {
        'order_id' : order.Order_Id,
        'product_details': product_details,
        'user_name': user.username,
        'user_fullname': user.first_name + " " + user.last_name,
        'user_email': user.email,
        'user_contact': customer.contact,
        'user_state': customer.state,
        'user_city': customer.city,
        'user_pincode': customer.pincode,
        'user_address': customer.address,
    }

    return render(request, 'Assets/OrderDetails.html', context)

@login_required
def MyOrders(request):
    user = request.user 
    orders = Order.objects.filter(user=user).distinct()  

    order_data = []

    for order in orders:
        ordered_items = order.Items.filter(Ordered=True)

        for item in ordered_items:
            product_info = {
                'order_id': order.id,
                'name': item.Product.Product_Name,
                'price': item.Product.Price,
                'size': item.size,
                'image': item.Product.Product_Image.url,
                'quantity': item.Quantity,
                'Order_Delivered': item.Order_Delivered,
                'Order_Delivered': item.Order_Delivered,
                'Category': item.Product.Category,
                'get_total_item_price': item.get_total_item_price(),
            }
            order_data.append(product_info)

    context = {
        'order_data': order_data,
    }

    return render(request, 'Assets/MyOrders.html', context)