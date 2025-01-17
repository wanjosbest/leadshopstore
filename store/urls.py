from django.urls import path
from .import views



urlpatterns =[
     path("register/", views.register_view, name="register"),
     path("login/", views.login_view, name="login"), 
     path("logout/", views.logout_view, name="logout"),
     path("profile/<username>/",views.user_profile, name="user_profile"),
     path("delete-account/", views.deleteacc, name="delete-account"),
     path('delete_user/<int:user_id>/', views.delete_user_view, name='delete_user'),
     path('password/change/', views.change_password, name='password_change'),
     path('password/done/', views.password_change_done, name='password_change_done'),
     path("", views.index, name="index"),
     path("search/", views.search, name="search"),
     #path("category/<sub_category>/", views.product_category, name="product_category"),
     path("all-products/", views.product_listView, name = "product_list"),
     path("product/<slug>/", views.product_detailView, name="product_detail"),
     path('password_reset/', views.password_reset_request, name='password_reset'),
     path('password_reset/done/', views.password_reset_done, name='password_reset_done'),
     path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
     path('reset/done/', views.password_reset_complete, name='password_reset_complete'),
     path('cartlist/', views.cartlist, name='cartlist'),
    # path('cart/add/<int:id>/', views.add_to_cart, name='add_to_cart'),
     path("checkout/", views.shipping_details, name="checkout"),
     path('cart/', views.view_cart, name='view_cart'),
     path("remove_cart/<int:item_id>/",views.remove_from_cart, name="remove_cart"),
     path("category-list/", views.category_listView, name = "category_list"),
     path("category-details/<str:id>/", views.category_detailView, name="category_detail"),
     path("subcategory-products/<int:id>/", views.products_by_subcategory, name="productsby_category"),
     path('cart/checkout/', views.initialize_payment, name='initialize_payment'),
     path('payment/verify/', views.verify_payment, name='verify_payment'),
     path('webhook/paystack/', views.paystack_webhook, name='paystack_webhook'),
     path('order-history/<username>/', views.order_history_view, name='order_history'),
     path("addproduct/", views.addproducts, name="addproducts"),
     path("userproducts/", views.userproductlist, name="userproductlist"),
     path("users/", views.getalluser, name="allusers"),
     path("user-address/<username>/", views.useraddress, name="user-address"),
     path("editaddres/<username>/",views.editaddress, name="editaddress"),
     path("editprofile/<username>/",views.editprofile, name="editprofile"),
     path("admin-access/", views.adminlightdasboardview, name="adminlightdashboardview"),
     path("delete-product/<product_id>/",views.admindeleteproducts, name= "admin-deleteproduct"),
     path("pages/<slug:slug>/",views.staticpages, name="static-pages"),
     
   
]