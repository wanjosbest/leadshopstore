from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import PasswordChangeForm
from .models import User,ShippingDetails

class ShippingDetailsForm(forms.ModelForm):
    class Meta:
        model = ShippingDetails
        fields = [
            'recipient_name', 'address_line_1', 'address_line_2',
            'city', 'state', 'postal_code', 'country', 'phone_number', 'email'
        ]
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