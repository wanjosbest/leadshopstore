from django.contrib.sitemaps import Sitemap
from .models import Products

class ProductSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    def items(self):
        return Products.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.updated
