from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Post(models.Model):
    """Example model that uses the custom user model."""
    
    title = models.CharField(_('title'), max_length=200)
    content = models.TextField(_('content'))
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts',
        verbose_name=_('author')
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Comment(models.Model):
    """Example model with foreign key to custom user."""
    
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('post')
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_comments',
        verbose_name=_('author')
    )
    content = models.TextField(_('content'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author.email} on {self.post.title}'