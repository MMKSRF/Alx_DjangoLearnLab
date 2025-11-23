from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.forms import ModelForm
from .models import Book

# Book Form
# Security: Using Django ModelForm ensures automatic validation and prevents SQL injection
# All user inputs are validated through Django's form validation system
class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']


# Permission-protected views
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    View to list all books. Requires can_view permission.
    
    Security: 
    - Uses Django ORM (Book.objects.all()) which prevents SQL injection
    - Permission check ensures only authorized users can access
    """
    books = Book.objects.all()  # Safe: Django ORM prevents SQL injection
    return render(request, 'bookshelf/book_list.html', {'books': books})


@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """
    View to create a new book. Requires can_create permission.
    
    Security:
    - CSRF protection via Django middleware (requires {% csrf_token %} in template)
    - Form validation prevents invalid data and SQL injection
    - Permission check ensures only authorized users can create books
    """
    if request.method == 'POST':
        form = BookForm(request.POST)  # Safe: Django forms handle input validation
        if form.is_valid():  # Validates and sanitizes all inputs
            form.save()  # Safe: Django ORM prevents SQL injection
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'bookshelf/book_form.html', {'form': form, 'action': 'Create'})


@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    """
    View to edit an existing book. Requires can_edit permission.
    
    Security:
    - get_object_or_404 safely handles invalid primary keys (prevents errors)
    - Django ORM parameterizes queries (pk=pk is safe from SQL injection)
    - Form validation ensures data integrity
    - CSRF protection via middleware
    """
    book = get_object_or_404(Book, pk=pk)  # Safe: Django ORM parameterizes queries
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)  # Safe: Form validation
        if form.is_valid():
            form.save()  # Safe: Django ORM prevents SQL injection
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/book_form.html', {'form': form, 'book': book, 'action': 'Edit'})


@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    """
    View to delete a book. Requires can_delete permission.
    
    Security:
    - Requires POST method to prevent accidental deletions via GET
    - get_object_or_404 safely handles invalid primary keys
    - Django ORM prevents SQL injection
    - Permission check ensures only authorized users can delete
    - CSRF protection via middleware
    """
    book = get_object_or_404(Book, pk=pk)  # Safe: Django ORM parameterizes queries
    if request.method == 'POST':  # Security: Only allow deletion via POST
        book.delete()  # Safe: Django ORM prevents SQL injection
        return redirect('book_list')
    return render(request, 'bookshelf/book_delete.html', {'book': book})
