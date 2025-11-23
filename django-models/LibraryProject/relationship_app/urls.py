from django.urls import path
from .views import list_books, LibraryDetailView, CustomLoginView, CustomLogoutView, register

urlpatterns = [
    # Function-Based View
    path('books/', list_books, name='list_books'),

    # Class-Based View
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    
    # Authentication URLs
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
]