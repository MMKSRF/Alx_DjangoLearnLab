from django.forms import ModelForm
from .models import Book

# Book Form
# Security: Using Django ModelForm ensures automatic validation and prevents SQL injection
# All user inputs are validated through Django's form validation system
class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']

