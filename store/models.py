from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse




#tutor register
class User(AbstractUser):
    email = models.EmailField(null =True, unique=True, max_length=100)
    address=models.CharField(max_length=300,null=True,blank=True)
    image = models.ImageField(upload_to="img", null=True,blank=True,default="user.jpg")

    class Meta:
        verbose_name="Users"
        verbose_name_plural="Users"

    def __str__(self):
        return self.username
    

class category(models.Model):
    name = models.CharField(max_length=30, null = True)
    image = models.ImageField(upload_to="img", null=True,unique=True)  
    slug = models.SlugField(null=True, max_length=100,unique=True)
   
    def __str__(self):
        return self.name
class Product_image(models.Model):
    name = models.CharField(max_length=50, null=True,unique=True)
    image = models.ImageField(upload_to="img", null=True,unique=True)
    
    def __str__(self):
        return self.name 
    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})
    
class subcategory(models.Model):
    category = models.ForeignKey(category, related_name="subcategory", on_delete= models.CASCADE, null=True)
    sub_category_name = models.CharField(max_length=30,null=True, unique=True, verbose_name="name")
    image = models.ForeignKey(Product_image, on_delete=models.CASCADE, related_name="sub_category_image", null=True)
 
    
    def __str__(self):
        return f"{self.sub_category_name} in {self.category} Category"
       
    
class Products(models.Model):
    STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    category = models.ForeignKey(subcategory, related_name="product_subcategory",on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=50, null =True)
    description = models.TextField(null =True)
    meta_keywords = models.CharField(max_length=255, null =True, help_text="seo keywords seprated with comma")
    meta_descriptions = models.CharField(max_length=255, null =True, help_text="seo description here")
    product_image = models.ForeignKey(Product_image, on_delete=models.CASCADE, related_name="Product_image", null= True)
    published = models.DateTimeField(auto_now_add =True, null=True)
    updated = models.DateTimeField(auto_now=True,null=True)
    slug = models.SlugField(null=True, max_length=100,unique=True)
    actualprice = models.DecimalField(max_digits= 20, decimal_places=2,null=True)
    discountedprice = models.DecimalField(max_digits= 20, decimal_places=2,null=True)
    status = models.CharField(max_length=30, null =True,choices = STATUS_CHOICES,default="published")
    additionalinfo = models.TextField(null =True)
    
    def __str__(self):
        return f"{self.name} "
    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})
class productfeatures(models.Model):
    product = models.ForeignKey(Products,related_name="productinfo",on_delete=models.CASCADE, null=True)
    feature = models.CharField(max_length=255, null=True)
    published = models.DateTimeField(auto_now_add =True, null=True)
    updated = models.DateTimeField(auto_now=True,null=True)
    
    def __str__(self):
        return f"{self.feature} of {self.product}"
    
class carousel (models.Model):
    carousel_title = models.CharField(max_length=255,null=True)
    carousel_one_product=models.ForeignKey(Products, related_name="carousel_one_products",on_delete=models.CASCADE, null=True)
    carousel_one_title =models.CharField(max_length=100, null =True)
    carousel_one_description = models.TextField(null=True)
    carousel_one_image = models.ImageField(upload_to = "img", null=True)
    carousel_two_product=models.ForeignKey(Products, related_name="carousel_two_products",on_delete=models.CASCADE, null=True)
    carousel_two_title =models.CharField(max_length=100, null =True)
    carousel_two_description = models.TextField(null=True)
    carousel_two_image = models.ImageField(upload_to = "img", null=True)
    carousel_three_product=models.ForeignKey(Products, related_name="carousel_three_products",on_delete=models.CASCADE, null=True)
    carousel_three_title =models.CharField(max_length=100, null =True)
    carousel_three_description = models.TextField(null=True)
    carousel_three_image = models.ImageField(upload_to = "img", null=True)
    
    def __str__(self):
        return self.carousel_title
    
class special_offer(models.Model):
    title = models.CharField(max_length=255,null=True)
    spclofferonetitle = models.CharField(max_length=255,null=True)
    spclofferoneproduct = models.ForeignKey(Products, related_name="spclofferone_products",on_delete=models.CASCADE, null=True)
    spclofferonecommission =models.CharField(max_length=20,null=True)
    spclofferoneimage = models.ImageField(upload_to = "img", null=True)
    spcloffertwotitle = models.CharField(max_length=255,null=True)
    spcloffertwoproduct = models.ForeignKey(Products, related_name="spcloffertwo_products",on_delete=models.CASCADE, null=True)
    spcloffertwocommission =models.CharField(max_length=20,null=True)
    spcloffertwoimage = models.ImageField(upload_to = "img", null=True)
    
    def __str__(self):
        return self.title
    
#featured products

class featured_products(models.Model):
    product =models.ForeignKey(Products, related_name="featured_image_products",on_delete=models.CASCADE, null=True)
    name =models.CharField(max_length=100,null=True)
    image =models.ForeignKey(Product_image, on_delete=models.CASCADE, related_name="fetured_product_image", null=True)
    actualprice = models.CharField(max_length=20,null=True)
    discountedprice = models.CharField(max_length=20,null=True)
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False) 
    

    def __str__(self):
        return f"Cart of {self.user.username}"
    
class CartItem(models.Model):
    
    cart = models.ForeignKey(Cart,null=True, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Products,null=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, null=True)
    published = models.DateTimeField(auto_now_add =True, null=True)
    
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    def get_total_price(self):
        return self.quantity * self.product.discountedprice

class Order(models.Model):
    product = models.ForeignKey(Products,null=True, on_delete=models.CASCADE)
    customer_email = models.EmailField(null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount to be paid
    reference = models.CharField(max_length=200, unique=True)  # Unique Paystack reference
    verified = models.BooleanField(default=False)  # Payment verification status
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} for {self.product.name}"
    
#add review 

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    name =models.CharField(max_length=50,null=True)
    product = models.ForeignKey(Products,null=True, on_delete=models.CASCADE)
    review = models.TextField(null=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    email = models.EmailField(null=True)
    def __str__ (self):
        return f"{self.product} Review By {self.name}"
   
class ShippingDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)  # link to user
    recipient_name = models.CharField(max_length=255,null=True)
    address_line_1 = models.CharField(max_length=255,null=True)
    address_line_2 = models.CharField(max_length=255, blank=True,null=True)
    city = models.CharField(max_length=100,null=True)
    state = models.CharField(max_length=100,null=True)
    postal_code = models.CharField(max_length=20,null=True)
    country = models.CharField(max_length=100,null=True)
    phone_number = models.CharField(max_length=20,null=True)
    email = models.EmailField(null=True)

    def __str__(self):
        return f"{self.recipient_name} - {self.city}, {self.country}"
class OrderHistory(models.Model):
    order_status =(
        ("delivered","delivered"),
        ("purchased", "purchased"),
       
        )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    customer_email = models.EmailField(null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=order_status, default="purchased")
    product = models.ForeignKey(Products,null=True, on_delete=models.CASCADE, related_name="product_status") 

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"
# purchased products


