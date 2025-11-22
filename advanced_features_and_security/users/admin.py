from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser
from .forms import CustomUserChangeForm, CustomUserCreationForm

class CustomUserAdmin(UserAdmin):
    """Define admin model for custom User model with no username field."""
    
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    model = CustomUser
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {
            'fields': (
                'first_name', 
                'last_name', 
                'date_of_birth', 
                'profile_photo'
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_active', 
                'is_staff', 
                'is_superuser',
                'groups', 
                'user_permissions'
            ),
        }),
        (_('Important dates'), {
            'fields': (
                'last_login', 
                'date_joined'
            )
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 
                'password1', 
                'password2',
                'first_name',
                'last_name',
                'date_of_birth',
                'profile_photo'
            ),
        }),
    )
    
    list_display = (
        'email', 
        'first_name', 
        'last_name', 
        'date_of_birth',
        'is_staff'
    )
    
    list_filter = (
        'is_staff', 
        'is_superuser', 
        'is_active', 
        'groups',
        'date_of_birth'
    )
    
    search_fields = (
        'email', 
        'first_name', 
        'last_name'
    )
    
    ordering = ('email',)
    
    filter_horizontal = (
        'groups', 
        'user_permissions',
    )

admin.site.register(CustomUser, CustomUserAdmin)