from django.shortcuts import render,HttpResponse, redirect,get_object_or_404
from .models import (User,Products, carousel,special_offer,category,featured_products,subcategory,CartItem,Order,Cart,
                     Review,ShippingDetails, OrderHistory,Pages)
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.views.generic import ListView,DetailView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
import uuid
from uuid import uuid4
import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from .forms import PasswordResetRequestForm, CustomSetPasswordForm,PasswordChangeForm,ShippingDetailsForm,ProductForm
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator


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
@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('/login/')

#fogort password
@login_required(login_url= '/login/',redirect_field_name="next")
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Keeps the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password_change_done')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user=request.user)
    
    return render(request, 'user/change_password.html', {'form': form})

def password_change_done(request):
    return render(request, 'user/change_password_done.html')
   


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
          messages.info(request, "Product added to cart Succesfully")

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
def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            users = User.objects.filter(email=email)
            if users.exists():
                for user in users:
                    subject = "Password Reset Requested"
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    token = default_token_generator.make_token(user)
                    domain = get_current_site(request).domain
                    reset_link = reverse("password_reset_confirm", kwargs={"uidb64": uid, "token": token})
                    reset_url = f'https://{domain}{reset_link}'
                    message = f"Click the link below to reset your password: {reset_url}"
                    send_mail(subject, message, 'josephwandiyahyel3@gmail.com', [email])
                return redirect("password_reset_done")
            else:
                return HttpResponse("Please you are not our User")
    else:
        form = PasswordResetRequestForm()
    return render(request, "user/password_reset_request.html", {"form": form})


def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(get_user_model(), pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = CustomSetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect("password_reset_complete")
        else:
            form = CustomSetPasswordForm(user)
        return render(request, "user/password_reset_confirm.html", {"form": form})
    else:
        return render(request, "user/password_reset_invalid.html")
    
def password_reset_complete(request):
    return render(request, "user/password_reset_complete.html") 

def password_reset_done(request):
    return render(request, "user/password_reset_done.html")  



#user cart

def get_user_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart



#view cart
@login_required(login_url= '/login/',redirect_field_name="next")
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
    getuser = User.objects.get(username = request.user)
    allcartitems = CartItem.objects.filter(user=request.user)
    getcount = allcartitems.count()
    print(getcount)
    context ={
        "getcount":getcount, "getuser":getuser
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
@login_required(login_url='/login/', redirect_field_name="next")
def initialize_payment(request):
    # Fetch the user's cart
    cart = get_user_cart(request.user)  # Replace with your actual function to fetch the user's cart
    if not cart or not cart.items.exists():
        return render(request, 'products/payment_error.html', {'message': 'No active cart or cart is empty.'})
    
    # Calculate total price of items in the cart
    cart_items = cart.items.all()
    total_price = sum(item.get_total_price() for item in cart_items)
    if total_price <= 0:
        return render(request, 'products/payment_error.html', {'message': 'Cart is empty.'})

    # Generate a unique payment reference
    reference = f"PAY-{uuid4()}"  # Use UUID for unique and secure references

    # Prepare data for Paystack API
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',  # Ensure PAYSTACK_SECRET_KEY is in your settings.py
    }
    data = {
        'email': request.user.email,
        'amount': int(total_price * 100),  # Paystack requires the amount in kobo (smallest currency unit)
        'reference': reference,
        'callback_url': request.build_absolute_uri('/payment/verify/'),  # Ensure this URL is configured correctly
    }

    # Initialize transaction via Paystack API
    url = 'https://api.paystack.co/transaction/initialize/'
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        # On success, redirect user to Paystack payment page
        payment_url = response.json()['data']['authorization_url']
        return redirect(payment_url)
    else:
        # Handle API errors 
        error_message = response.json().get('message', 'An error occurred while initializing payment.')
        return render(request, 'products/payment_error.html', {'message': error_message})

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
            getquantity = CartItem.objects.filter(user=request.user)
            total_price = sum(item.product.discountedprice * item.quantity for item in cart_items)
            Quantity = getquantity.quantity
            savedetails = OrderHistory.objects.create(user = request.user, total_amount=total_price,customer_email = request.user.email, quantity = Quantity)
            savedetails.save()
            # Clear the cart items
            cart_items.delete()
            # Send a receipt email
            send_receipt_email(request.user.email, cart, result['amount'] / 100)
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
        'josephwandiyahyel3@gmail.com',  
        [email],
        fail_silently=False,
    )
    
@login_required(login_url= '/login/',redirect_field_name="next")
def shipping_details(request):
    try:
        # Try to get existing shipping details if any
        shipping = ShippingDetails.objects.get(user=request.user)
    except ShippingDetails.DoesNotExist:
        shipping = None

    if request.method == 'POST':
        form = ShippingDetailsForm(request.POST, instance=shipping)
        if form.is_valid():
            form.save()  # Save the shipping details
            return redirect("initialize_payment")  # Redirect to the checkout page
    else:
        form = ShippingDetailsForm(instance=shipping)

    return render(request, 'shipping_details.html', {'form': form})
@login_required(login_url= '/login/',redirect_field_name="next")
def user_profile(request,username):
    getuser = User.objects.filter(username = username)
    context = {"getuser":getuser}
    return render (request, "user/profile.html",context)
@login_required(login_url= '/login/',redirect_field_name="next")
def editprofile ( request, username):
    userprofiledata = User.objects.filter(username = username)
    try:
       address = User.objects.get(username = request.user) 
    except User.DoesNotExist:
       address = None
       
    if request.method =="POST":
       address.first_name = request.POST.get("firstname")
       address.last_name = request.POST.get("lastname")
       address.email = request.POST.get("email")
       address.save()
       messages.info(request,"Profile updated successfully")
    context = {"userprofiledata": userprofiledata}
    return render(request, "user/editprofile.html", context)

@login_required(login_url= '/login/',redirect_field_name="next")
def delete_user_view(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return HttpResponse(f"User with ID {user_id} has been deleted.")
    except User.DoesNotExist:
        return HttpResponse(f"User with ID {user_id} does not exist.", status=404)
    
@login_required(login_url= '/login/',redirect_field_name="next")
def deleteacc(request):
    return render(request, "user/deleteacc.html")

@login_required(login_url= '/login/',redirect_field_name="next")
def order_history_view(request, username):
    
    getuser = User.objects.get(username = username)
    orders = OrderHistory.objects.filter(user=getuser)
   
    return render(request, 'user/order_history.html', {'orders': orders})
    
    
# user to add products
@login_required(login_url= '/login/',redirect_field_name="next")
def addproducts(request):
    form = ProductForm(request.POST)
    if request.method =="POST":
       if form.is_valid():
          form.save()
       messages.info(request,"product added Successfully!")
    return render(request, "admin/addproducts.html",{"form":form})

# view product lists by user
def userproductlist(request):
    user = request.user
    getproduct = Products.objects.filter(user = user)
    
    context = {"getproduct":getproduct}
    return render(request, "user/userproductlist.html", context)

def getalluser(request):
    getusers = User.objects.all()
    context = {"getusers":getusers}
    print(getusers)
    return render(request, "allusers.html",context)
# user address

def useraddress(request, username):
  
    getuser = User.objects.filter(username = username)
    
    context = {"getuser":getuser}
    return render(request, 'user/address.html', context)

def editaddress(request, username):
    getuser = User.objects.filter(username = username)
    try:
       address = User.objects.get(username = request.user) 
    except User.DoesNotExist:
       address = None
       
    if request.method =="POST":
       address.address = request.POST.get("editaddress")
       address.save()
       messages.info(request,"Address updated successfully")
    context ={"getuser":getuser}
    return render(request, 'user/editaddress.html', context)
@login_required(login_url= '/login/',redirect_field_name="next")
def adminlightdasboardview(request):
    post = Products.objects.all() 
    # paginate products list
    paginator = Paginator(post, 2) # number of producsts to display per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context ={ "page_obj":page_obj}
    
    return render(request, "admin/adminlightdashboard.html",context)

@login_required(login_url= '/login/',redirect_field_name="next")
def admindeleteproducts(request, product_id):
    try:
        deleteproduct = Products.objects.get(id = product_id)
        deleteproduct.delete()
        
    except Products.DoesNotExist:
        messages.info(request,"product does'nt exist")
    return HttpResponse("Deleted successfully")

# i want to add trash later
    
def editproducts(request):
    user = request.user.is_superuser
    getproduct = Products.objects.filter(username = user)
    context = {"getproduct": getproduct}
    return render("admin/editproduct.html", context)
    
# about us page

def aboutus(request):
    Getpage = Pages.objects.filter(slug ="about-us")
    context = {"aboutus":Getpage}
    return render(request, "aboutus.html",context)