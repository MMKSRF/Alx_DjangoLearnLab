from rest_framework import generics, viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from .models import Book
from .serializers import BookSerializer


class BookList(generics.ListAPIView):
    """
    API endpoint that allows users to view a list of all books.
    This is a read-only endpoint that returns a list of all Book instances.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Book instances.
    
    Provides CRUD operations:
    - GET /books_all/ - List all books
    - GET /books_all/<id>/ - Retrieve a specific book
    - POST /books_all/ - Create a new book
    - PUT /books_all/<id>/ - Update a book (full update)
    - PATCH /books_all/<id>/ - Partial update of a book
    - DELETE /books_all/<id>/ - Delete a book
    
    Requires authentication to access.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
