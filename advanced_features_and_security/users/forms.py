from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """Form for creating new users in the admin panel."""
    
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )

    class Meta:
        model = CustomUser
        fields = (
            'email', 
            'first_name', 
            'last_name', 
            'date_of_birth', 
            'profile_photo'
        )
        field_classes = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True

class CustomUserChangeForm(UserChangeForm):
    """Form for updating users in the admin panel."""
    
    class Meta:
        model = CustomUser
        fields = '__all__'
        field_classes = {}