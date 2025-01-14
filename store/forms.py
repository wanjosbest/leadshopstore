from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import PasswordChangeForm
from .models import User,ShippingDetails, Products

class ShippingDetailsForm(forms.ModelForm):
    class Meta:
        model = ShippingDetails
        fields = [
            'recipient_name', 'address_line_1', 'address_line_2',
            'city', 'state', 'postal_code', 'country', 'phone_number', 'email'
        ]
        widgets = {
            'recipient_name': forms.TextInput(attrs={'class':'form-control'}),
            'address_line_1': forms.TextInput(attrs={'class':'form-control'}),
            'address_line_2': forms.TextInput(attrs={'class':'form-control'}),
            'city': forms.TextInput(attrs={'class':'form-control'}),
            'state': forms.TextInput(attrs={'class':'form-control'}),
            'postal_code': forms.TextInput(attrs={'class':'form-control'}),
            'country': forms.TextInput(attrs={'class':'form-control'}),
            'phone_number': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.TextInput(attrs={'class':'form-control'}),
        }
class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
    


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label="Email Address", max_length=254)
    
    
class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput,
        label=_("New Password"),
        help_text=_("Your new password must contain at least 8 characters."),
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput,
        label=_("Confirm Password"),
        help_text=_("Enter the same password as before, for verification."),
    )
    
class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ["user","name","category","meta_descriptions","meta_keywords","description","product_image","slug","actualprice","discountedprice","additionalinfo"]
        widgets ={
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'}),
            'meta_descriptions': forms.TextInput(attrs={'class':'form-control'}),
            'meta_keywords': forms.TextInput(attrs={'class':'form-control'}),
            'slug': forms.TextInput(attrs={'class':'form-control'}),
            'additionalinfo': forms.Textarea(attrs={'class':'form-control'}),
              
        }
