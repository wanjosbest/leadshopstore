
"""
from .models import footerpages

def footer_pages(request):
   
    return {
        'footer_pages': footerpages.objects.filter(is_visible=True)
    }
"""