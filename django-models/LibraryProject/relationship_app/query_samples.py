# 1. Query all books by a specific author
def books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        # ✅ Use filter() explicitly
        return Book.objects.filter(author=author)
    except Author.DoesNotExist:
        return []