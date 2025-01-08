from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.utils.translation import gettext_lazy as _

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    


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