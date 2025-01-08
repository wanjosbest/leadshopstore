from django.urls import path
from .import views



urlpatterns =[
     path("register/", views.register_view, name="register"),
     path("login/", views.login_view, name="login"), 
     path("logout/", views.logout_view, name="logout"),
     path("profile/",views.user_profile, name="user_profile"),
     
     path("delete-account/<int:user_id>/",views.userdeleteacc, name="delete-account"),
     path("change-password/", views.ChangePasswordView.as_view(), name="changepassword"),
     path("", views.index, name="index"),
     path("search/", views.search, name="search"),
     #path("category/<sub_category>/", views.product_category, name="product_category"),
     path("product-list", views.product_listView, name = "product_list"),
     path("product/<slug>/", views.product_detailView, name="product_detail"),
     path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
     path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
     path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
     path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
     path("shop", views.shop, name="shop"),
     path("shop-details", views.shopdetails, name="shopdetails"),
     path("contact", views.contact, name="contact-us"),
     path('cartlist/', views.cartlist, name='cartlist'),
    # path('cart/add/<int:id>/', views.add_to_cart, name='add_to_cart'),
     path("checkout/", views.checkoutform, name="checkout"),
     path('cart/', views.view_cart, name='view_cart'),
     path("remove_cart/<int:item_id>/",views.remove_from_cart, name="remove_cart"),
     path("category-list/", views.category_listView, name = "category_list"),
     path("category-details/<str:id>/", views.category_detailView, name="category_detail"),
     path("subcategory-products/<int:id>/", views.products_by_subcategory, name="productsby_category"),
     path('cart/checkout/', views.initialize_payment, name='initialize_payment'),
     path('payment/verify/', views.verify_payment, name='verify_payment'),
     path('webhook/paystack/', views.paystack_webhook, name='paystack_webhook'),
     path('order-history/', views.order_history_view, name='order_history'),
      
    
]