from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import BookList, BookViewSet

# Initialize router for ViewSet
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Token authentication endpoint - POST /api/api-token-auth/
    # Send username and password to obtain an authentication token
    # Format: {"username": "user", "password": "pass"}
    path('api-token-auth/', obtain_auth_token, name='api-token-auth'),
    
    # Route for the BookList view (ListAPIView) - GET /api/books/
    path('books/', BookList.as_view(), name='book-list'),
    
    # Include the router URLs for BookViewSet (all CRUD operations)
    # This includes routes like /api/books_all/, /api/books_all/<id>/, etc.
    path('', include(router.urls)),
]
