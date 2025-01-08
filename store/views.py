from django.shortcuts import render,HttpResponse, redirect,get_object_or_404
from .models import (User,Products, carousel,special_offer,category,featured_products,subcategory,CartItem,Order,Cart,
                     Review,shippingdetails, OrderHistory)
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.views.generic import ListView,DetailView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
import uuid
import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
def index(request):
    getcouroseldetails = carousel.objects.all()
    getspecialoffers = special_offer.objects.all()
    getcategory = category.objects.all()
    getfeaturedproducts = featured_products.objects.all()
    
    #get recent products
    # [:8] is the maximum number of recent products that will be displayed
    getrecentproduct = Products.objects.all().order_by("-published")[:8]
    
    context = {
        "carouseldetail":getcouroseldetails, "specialoffer":getspecialoffers, "getcategory":getcategory,"featuredproducts":getfeaturedproducts,
        "getrecentproduct":getrecentproduct
    }
    return render (request,"index.html", context)


def register_view(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        address = request.POST.get('address')
        image = request.FILES.get("image")
        # Check if a user with the provided username already exists
        user = User.objects.filter(username=username)
        
        if user.exists():
            # Display an information message if the username is taken
            messages.info(request, "Username already taken!")
            return redirect('/register/')
        
        # Create a new User object with the provided information
        user = User.objects.create_user(
            first_name=firstname,
            last_name=lastname,
            username=username,
            email = email,
            address = address,
            image = image
        )
        #encript password
        user.set_password(password)
        #save user
        user.save()
        # Display an information message indicating successful account creation
        messages.info(request, "Account created Successfully!")
        return redirect('/login/')
    
    # Render the registration page template (GET request)
    return render(request, 'user/register.html')


# logiin user
def login_view(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if a user with the provided username exists
        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid Username')
            return redirect('/login/')
        user = authenticate(username=username, password=password)
        
        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('/login/')
        else:
            login(request,user)
            return redirect("view_cart")
    return render(request, 'user/login.html')
# logout user

def logout_view(request):
    logout(request)
    return redirect('/login/')

#fogort password
class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('index')
    template_name = 'user/change_password.html'
   


# search products 

def search(request):
    if request.method =="POST":
       searched = request.POST.get("searched")
       searched = Products.objects.filter(name__icontains = searched)
       return render(request, "header.html",{"searched":searched}) 
    else:
      return render(request, "header.html") 
    
    
# get posts by category

def product_category(request, sub_category):
    products = Products.objects.filter(category = sub_category)
    context = {
        
        'category':sub_category, "products":products
    }
    
    return render (request, "products/category.html", context)
  #product list view
def product_listView(request):
    listall_products = Products.objects.all().order_by("-published")
    context ={
        "all_products":listall_products
    }
    return render(request, "products/product_list.html", context)
#product detail view
def product_detailView(request, slug):
    productdetails = Products.objects.get(slug = slug)
    if request.method=="POST":
       Quantity = request.POST.get("quantity")
       product = request.POST.get("product")
       cart = get_user_cart(request.user)

    # Check if the product is already in the cart
       cart_item, created = CartItem.objects.get_or_create(cart=cart,product_id=product,quantity=Quantity)
       if not created:
        # If the product is already in the cart, increase the quantity
          cart_item.quantity += 1
          cart_item.save()

    context ={
        "product_details": productdetails
        
    }
    return render(request, "products/product_detail.html",context)

def reviewView(request, slug):
    productdetails = Products.objects.get(slug = slug)
    getreview = Review.objects.filter(product =productdetails).order_by("-date_added")
    get_numberofreviews = getreview.count()
     #get user reviews
    if request.method=="POST":
       reviewuser = request.user
       name = request.POST.get("name")
       reviewuseremail = request.POST.get("email")
       reviewedproduct = productdetails.id
       review = request.POST.get("review")
       savereview = Review.objects.create(user = reviewuser, email=reviewuseremail, review = review, product_id = reviewedproduct, name = name)
       savereview.save()
       return redirect(f"/product-details/{slug}/")
    context = {
        "getreview":getreview,"get_numberofreviews":get_numberofreviews
    }
    return render(request, "products/product_detail.html", context)

# Password reset request view
class CustomPasswordResetView(PasswordResetView):
    template_name = 'user/password_reset.html'
    email_template_name = 'user/password_reset_email.html'
    subject_template_name = 'user/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

# Password reset done view
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'user/password_reset_done.html'

# Password reset confirm view
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'user/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')
# Password reset complete view
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'user/password_reset_complete.html'
    
# shop

def shop(request):
    
    return render(request, "shop.html")

def shopdetails(request):
    
    return render(request, "shopdetail.html")
def contact(request):
    
    return render(request, "contact.html")

#user cart
def get_user_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart



#view cart
@login_required
def view_cart(request):
    cart = get_user_cart(request.user)
    cart_items = cart.items.all()
    total_price = sum(item.get_total_price() for item in cart_items)
   
    return render(request, 'products/view_cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })
    
#cartlist
def cartlist(request):
    allcartitems = CartItem.objects.all()
    context ={
        "allcartitems":allcartitems
    }
    return render(request, "products/cart_list.html", context)
#delete cart
def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('view_cart')
#cart details

def cart(request, id):
    cartdetails = CartItem.objects.get(id = id)
    cart_items = CartItem.objects.filter(user=request.user)
    allitems = CartItem.objects.all()
    product_id = Products.objects.all()
    total_price = sum(item.product.discountedprice * item.quantity for item in cart_items)
    context = {
        "cartdetails":cartdetails," cart_items": cart_items, "total_price":total_price,"allitems":allitems,"product_id":product_id
    }
    return render(request, 'products/cart_detail.html', context)



def category_listView(request):
    listall_subcategory = category.objects.all()
    context ={
        "all_subcategory":listall_subcategory
    }
    return render(request, "products/category.html", context)
def category_detailView(request, id):
    categorydetails = subcategory.objects.get(id =id )
    #getproductposts by subcategory
    getproductbycategory = Products.objects.filter(category = categorydetails)
    context ={
        "category_details": categorydetails,"productsbycategory":getproductbycategory
    }
    return render(request, "products/category_detail.html",context)

def header(request):
    allcartitems = CartItem.objects.filter(user=request.user)
    
    getcount = allcartitems.count()
    print(getcount)
    context ={
        "getcount":getcount
    }
    return render(request, "header.html",context)

def products_by_subcategory(request,id):
    Subcategory = get_object_or_404(subcategory, id=id)
    products = Products.objects.filter(category=Subcategory)
    context = {
        'subcategory': Subcategory, 'products': products
        }
    return render(request, 'products_by_subcategory.html', context)

def generate_reference():
    return str(uuid.uuid4())

def totalamount(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.discountedprice * item.quantity for item in cart_items)
    return total_price
    

#initialize payment

def initialize_payment(request):
    cart = get_user_cart(request.user)
    cart_items = cart.items.all()
    total_price = sum(item.get_total_price() for item in cart_items)

    if total_price <= 0:
        return render(request, 'products/payment_error.html', {'message': 'Cart is empty.'})

    # Generate payment reference (can use UUID or similar)
    reference = f"PAY-{cart.id}-{request.user.id}"

    # Prepare data for Paystack API
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
    }
    data = {
        'email': request.user.email,
        'amount': int(total_price * 100),  # Paystack requires amount in kobo
        'reference': reference,
        'callback_url': request.build_absolute_uri('/payment/verify/'),  # Redirect here after payment
    }

    url = 'https://api.paystack.co/transaction/initialize'
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        payment_url = response.json()['data']['authorization_url']
        return redirect(payment_url)
    else:
        return render(request, 'products/payment_error.html', {'message': 'Payment initialization failed.'})

#verify payments

def verify_payment(request):
    reference = request.GET.get('reference')

    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
    }
    url = f'https://api.paystack.co/transaction/verify/{reference}'

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        result = response.json()['data']

        if result['status'] == 'success':
            # Fetch the cart using metadata or session data
            cart = Cart.objects.get(user=request.user, paid=False)
            cart_items = cart.items.all()

            # Mark the cart as paid
            cart.paid = True
            cart.save()

            # Clear the cart items
            cart_items.delete()

            # Send a receipt email
            send_receipt_email(request.user.email, cart, result['amount'] / 100)
            total_price = sum(item.get_total_price() for item in cart_items)
            savedetails = OrderHistory.objects.create(user = request.user, total_amount=total_price)
            savedetails.save()
            return render(request, 'products/payment_success.html', {'cart': cart})

    return render(request, 'products/payment_error.html', {'message': 'Payment verification failed.'})

#webhook

@csrf_exempt
def paystack_webhook(request):
    payload = json.loads(request.body)

    if payload['event'] == 'charge.success':
        reference = payload['data']['reference']
        cart_id = payload['data']['metadata']['cart_id']
        cart = Cart.objects.filter(id=cart_id).first()

        if cart:
            cart.paid = True
            cart.save()

    return HttpResponse(status=200)

#send receipt to email
def send_receipt_email(email, cart, total_amount):
    subject = "Payment Receipt"
    message = render_to_string('products/email_receipt.html', {
        'cart': cart,
        'total_amount': total_amount,
    })

    send_mail(
        subject,
        message,
        'josephwandiyahyel3@gmail.com',  # Replace with your sender email
        [email],
        fail_silently=False,
    )
    
def checkoutform(request):
    if request.method=="POST":
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        address = request.POST.get("address")
        state = request.POST.get("state")
        city = request.POST.get("city")
        cart = get_user_cart(request.user)
        user = request.user
        savedetails = shippingdetails.objects.create(fullname=fullname,email=email,address=address,state=state,cart=cart,user=user,city=city)
        savedetails.save()
        return redirect("initialize_payment")
    return render(request, "checkoutform.html")

def user_profile(request):
    getuser = request.user
    
    context = {"getuser":getuser}
    return render (request, "user/profile.html",context)

def userdeleteacc(request,user_id):
    getuser = User.objects.get(id = user_id)
    deleteacc = getuser.delete()
    context ={
        "getuser":getuser
    }
    return HttpResponse("Hey Account Deleted Successfully!")
   
@login_required
def order_history_view(request):
    orders = OrderHistory.objects.filter(user=request.user)
    return render(request, 'user/order_history.html', {'orders': orders})
    
