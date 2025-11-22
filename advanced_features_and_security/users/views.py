from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm

def register(request):
    """User registration view using custom user model."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Account created for {email}!')
                return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})