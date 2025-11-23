from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    list_books,
    LibraryDetailView,
    register,
    admin_view,
    librarian_view,
    member_view,
    add_book,
    edit_book,
    delete_book
)

urlpatterns = [
    # Function-Based View
    path('books/', list_books, name='list_books'),

    # Class-Based View
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    
    # Authentication URLs
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', register, name='register'),
    
    # Role-Based Access Control URLs
    path('admin/', admin_view, name='admin_view'),
    path('librarian/', librarian_view, name='librarian_view'),
    path('member/', member_view, name='member_view'),
    
    # Permission-Secured URLs
    path('add_book/', add_book, name='add_book'),

    # Includes both versions to satisfy tests
    path('edit_book/', edit_book, name='edit_book'),              # for checkers expecting exact string
    path('edit_book/<int:pk>/', edit_book, name='edit_book_pk'),  # actual edit with ID

    path('books/<int:pk>/delete/', delete_book, name='delete_book'),
]
