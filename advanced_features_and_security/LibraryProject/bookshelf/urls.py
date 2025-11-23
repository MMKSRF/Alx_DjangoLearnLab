from django.urls import path
from . import views

urlpatterns = [
    path('bookshelf/', views.book_list, name='book_list'),
    path('bookshelf/create/', views.book_create, name='book_create'),
    path('bookshelf/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('bookshelf/<int:pk>/delete/', views.book_delete, name='book_delete'),
    path('bookshelf/form-example/', views.form_example, name='form_example'),
]

