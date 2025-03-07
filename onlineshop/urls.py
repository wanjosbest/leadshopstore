"""
URL configuration for onlineshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap 
from store.sitemaps import ProductSitemap


urlpatterns = [
    path('admin/access/', admin.site.urls),
    path('admin/', admin.site.urls),
    path("", include("store.urls")),
    path('sitemap.xml', sitemap, {'sitemaps': {'article' : ProductSitemap}},),
  ]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "Lead Store Shop"
admin.site.site_title = "Lead Store Shop"
admin.site.index_title = "Lead Store Shop Admin"