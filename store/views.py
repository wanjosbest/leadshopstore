from django.shortcuts import render,HttpResponse, redirect
from .models import User,Products, carousel,special_offer,category,featured_products
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.views.generic import ListView,DetailView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy

def index(request):
    getcouroseldetails = carousel.objects.all()
    getspecialoffers = special_offer.objects.all()
    getcategory = category.objects.all()
    getfeaturedproducts = featured_products.objects.all()
    #get recent products
    getrecentproduct = Products.objects.all().order_by("-published")
    
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
            address = address
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
            return redirect("/")
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
      return render(request, "search.html") 
    
    
# get posts by category

def product_category(request, category):
    products = Products.objects.filter(category__name__icontains = category)
    context = {
        
        'category':category, "products":products
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
    context ={
        "product_details": productdetails
    }
    return render(request, "products/product_detail.html",context)

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




            