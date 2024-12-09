from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse




#tutor register
class User(AbstractUser):
    
    email = models.EmailField(null =True, unique=True, max_length=100)
    address=models.CharField(max_length=300,null=True,blank=True)


    class Meta:
        verbose_name="Users"
        verbose_name_plural="Users"

    def __str__(self):
        return self.username
    

class category(models.Model):
    name = models.CharField(max_length=30, null = True)
    image = models.ImageField(upload_to ="img",null=True)
    
    def __str__(self):
        return self.name
    
class subcategory(models.Model):
    category = models.ForeignKey(category, related_name="subcategory", on_delete= models.CASCADE, null=True)
    sub_category_name = models.CharField(max_length=30,null=True, unique=True, verbose_name="name")
    
    def __str__(self):
        return f"{self.sub_category_name} in {self.category} Category"
    
class Products(models.Model):
    category = models.ForeignKey(category, related_name="product_category",on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=50, null =True)
    description = models.TextField(null =True)
    meta_keywords = models.CharField(max_length=255, null =True, help_text="seo keywords seprated with comma")
    meta_descriptions = models.TextField(null =True, help_text="seo descriptions here ")
    product_image = models.ImageField(upload_to ="img")
    published = models.DateTimeField(auto_now_add =True, null=True)
    updated = models.DateTimeField(auto_now=True,null=True)
    slug = models.SlugField(null=True, max_length=100,unique=True)
    actualprice = models.CharField(max_length=20,null=True)
    discountedprice = models.CharField(max_length=20,null=True)
    
    def __str__(self):
        return f"{self.name} "
    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})
    
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
    image =models.ImageField(upload_to = "img", null=True)
    actualprice = models.CharField(max_length=20,null=True)
    discountedprice = models.CharField(max_length=20,null=True)
    def __str__(self):
        return self.name
    
    