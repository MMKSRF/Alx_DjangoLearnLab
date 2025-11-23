# Permissions and Groups Documentation

## Overview
This Django application implements a permission-based access control system using Django's built-in permissions and groups functionality. The system allows fine-grained control over who can perform specific actions on books in the library system.

## Custom Permissions

The `Book` model in the `bookshelf` app defines four custom permissions:

- **can_view**: Allows users to view books
- **can_create**: Allows users to create new books
- **can_edit**: Allows users to edit existing books
- **can_delete**: Allows users to delete books

These permissions are defined in `bookshelf/models.py` in the `Book` model's `Meta` class.

## User Groups

Three groups have been set up to organize users by their access levels:

### 1. Viewers
- **Permissions**: `can_view`
- **Capabilities**: Can only view books in the system
- **Use Case**: Regular users who should only be able to browse the book catalog

### 2. Editors
- **Permissions**: `can_view`, `can_create`, `can_edit`
- **Capabilities**: Can view, create, and edit books, but cannot delete them
- **Use Case**: Librarians or content managers who manage the book collection but shouldn't have delete privileges

### 3. Admins
- **Permissions**: `can_view`, `can_create`, `can_edit`, `can_delete`
- **Capabilities**: Full access to all book operations
- **Use Case**: Administrators who need complete control over the book management system

## Setting Up Groups

To set up the groups with their assigned permissions, run the management command:

```bash
python manage.py setup_groups
```

This command will:
1. Create the three groups (Viewers, Editors, Admins) if they don't exist
2. Assign the appropriate permissions to each group
3. Display a success message confirming the setup

## Assigning Users to Groups

Users can be assigned to groups through:
1. **Django Admin Interface**: Navigate to Users → Select a user → Add to Groups section
2. **Programmatically**: 
   ```python
   from django.contrib.auth.models import Group
   user = CustomUser.objects.get(username='username')
   group = Group.objects.get(name='Editors')
   user.groups.add(group)
   ```

## Permission Enforcement in Views

Permissions are enforced in views using the `@permission_required` decorator:

- `book_list`: Requires `bookshelf.can_view`
- `book_create`: Requires `bookshelf.can_create`
- `book_edit`: Requires `bookshelf.can_edit`
- `book_delete`: Requires `bookshelf.can_delete`

Example:
```python
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    # View implementation
```

The `raise_exception=True` parameter ensures that users without the required permission receive a 403 Forbidden error instead of being redirected to the login page.

## Testing Permissions

To test the permission system:

1. Create test users:
   ```python
   python manage.py shell
   from bookshelf.models import CustomUser
   from django.contrib.auth.models import Group
   
   viewer = CustomUser.objects.create_user('viewer', 'viewer@test.com', 'password')
   editor = CustomUser.objects.create_user('editor', 'editor@test.com', 'password')
   admin = CustomUser.objects.create_user('admin', 'admin@test.com', 'password')
   ```

2. Assign users to groups:
   ```python
   viewers_group = Group.objects.get(name='Viewers')
   editors_group = Group.objects.get(name='Editors')
   admins_group = Group.objects.get(name='Admins')
   
   viewer.groups.add(viewers_group)
   editor.groups.add(editors_group)
   admin.groups.add(admins_group)
   ```

3. Log in as each user and test access:
   - Viewer should only be able to view books
   - Editor should be able to view, create, and edit books
   - Admin should have full access to all operations

## Template Permission Checks

Templates can also check permissions using the `perms` template variable:

```django
{% if perms.bookshelf.can_create %}
    <a href="{% url 'book_create' %}">Add New Book</a>
{% endif %}
```

This allows conditional rendering of UI elements based on user permissions.

## Notes

- Permissions are checked at the view level, ensuring security even if templates are modified
- The permission system integrates seamlessly with Django's authentication system
- Groups can be managed through the Django admin interface
- Individual permissions can also be assigned directly to users if needed

