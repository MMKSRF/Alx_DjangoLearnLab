# delete.md

>>> book = Book.objects.get(title="Nineteen Eighty-Four")
>>> book.delete()
(1, {'bookshelf.Book': 1})
>>> Book.objects.all()
["from bookshelf.models import Book"]
<QuerySet []>

# The book was deleted successfully.