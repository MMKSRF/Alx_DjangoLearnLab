"""
Content Security Policy (CSP) Middleware

This middleware adds Content Security Policy headers to responses to help prevent
cross-site scripting (XSS) attacks by specifying which domains can be used to
load content in the application.
"""
from django.utils.deprecation import MiddlewareMixin


class CSPMiddleware(MiddlewareMixin):
    """
    Middleware to add Content Security Policy headers to responses.
    
    CSP helps prevent XSS attacks by controlling which resources can be loaded
    and executed on the page. This is a basic implementation.
    
    For production, consider using django-csp package for more advanced configuration.
    """
    
    def process_response(self, request, response):
        # Basic CSP policy
        # 'self' allows resources from the same origin
        # 'unsafe-inline' is needed for Django's inline scripts/styles (use with caution)
        # In production, consider removing 'unsafe-inline' and using nonces or hashes
        csp_policy = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"
        )
        
        response['Content-Security-Policy'] = csp_policy
        return response

