from django.urls import path
from .import views



urlpatterns =[
     path("register/", views.register_view, name="register"),
     path("login/", views.login_view, name="login"), 
     path("logout/", views.logout_view, name="logout"),
     path("change-password/", views.ChangePasswordView.as_view(), name="changepassword"),
     path("", views.index, name="index"),
     path("search/", views.search, name="search"),
     path("category/<category>/", views.product_category, name="product_category"),
     path("product-list", views.product_listView, name = "product_list"),
     path("product-details/<slug>/", views.product_detailView, name="product_detail"),
     path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
     path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
     path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
     path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
     path("shop", views.shop, name="shop"),
     path("shop-details", views.shopdetails, name="shopdetails"),
     path("contact-us", views.contact, name="contact-us"),
    
]