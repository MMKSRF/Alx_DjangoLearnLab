# HTTPS Deployment Configuration Guide

This document provides instructions for configuring HTTPS and secure redirects for the Django Library Project in a production environment.

## Overview

The application is configured with security settings that support HTTPS. This guide covers:
1. SSL/TLS Certificate Setup
2. Django Settings Configuration
3. Web Server Configuration (Nginx/Apache)
4. Security Headers Verification
5. Testing and Validation

## Prerequisites

- Django application deployed on a server
- Domain name configured
- Root or sudo access to the server
- Basic knowledge of web server configuration

## Step 1: Obtain SSL/TLS Certificate

### Option A: Let's Encrypt (Recommended - Free)

1. **Install Certbot**:
   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install certbot python3-certbot-nginx
   # or for Apache
   sudo apt-get install certbot python3-certbot-apache
   ```

2. **Obtain Certificate**:
   ```bash
   # For Nginx
   sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
   
   # For Apache
   sudo certbot --apache -d yourdomain.com -d www.yourdomain.com
   
   # Standalone (if not using Nginx/Apache)
   sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com
   ```

3. **Auto-renewal Setup**:
   Certbot automatically sets up a cron job for renewal. Verify:
   ```bash
   sudo certbot renew --dry-run
   ```

### Option B: Commercial Certificate

If using a commercial SSL certificate:
1. Purchase certificate from a Certificate Authority (CA)
2. Generate Certificate Signing Request (CSR)
3. Install certificate files on server

## Step 2: Update Django Settings

Update `LibraryProject/settings.py` for production:

```python
# Security settings for production with HTTPS
DEBUG = False

ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com', 'your-ip-address']

# HTTPS and Secure Redirects
SECURE_SSL_REDIRECT = True  # Redirect all HTTP to HTTPS
SECURE_HSTS_SECONDS = 31536000  # 1 year (in seconds)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Include subdomains in HSTS
SECURE_HSTS_PRELOAD = True  # Allow HSTS preload

# Secure Cookies (only sent over HTTPS)
SESSION_COOKIE_SECURE = True  # Session cookies only over HTTPS
CSRF_COOKIE_SECURE = True  # CSRF cookies only over HTTPS

# Additional Security Headers (already configured)
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
```

### Environment-Based Configuration

For better security, use environment variables:

```python
import os

DEBUG = os.environ.get('DEBUG', 'False') == 'True'
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True') == 'True'
SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', '31536000'))
```

## Step 3: Web Server Configuration

### Nginx Configuration

Create or update `/etc/nginx/sites-available/libraryproject`:

```nginx
# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS Server Block
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Certificate Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # SSL Configuration (Modern, Secure)
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Static Files
    location /static/ {
        alias /path/to/your/project/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Media Files
    location /media/ {
        alias /path/to/your/project/media/;
        expires 7d;
    }

    # Django Application
    location / {
        proxy_pass http://127.0.0.1:8000;  # Adjust port if using different WSGI server
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/libraryproject /etc/nginx/sites-enabled/
sudo nginx -t  # Test configuration
sudo systemctl reload nginx
```

### Apache Configuration

Create or update `/etc/apache2/sites-available/libraryproject.conf`:

```apache
# Redirect HTTP to HTTPS
<VirtualHost *:80>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com
    Redirect permanent / https://yourdomain.com/
</VirtualHost>

# HTTPS Virtual Host
<VirtualHost *:443>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com

    # SSL Configuration
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/yourdomain.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/yourdomain.com/privkey.pem

    # Security Headers
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
    Header always set X-Frame-Options "DENY"
    Header always set X-Content-Type-Options "nosniff"
    Header always set X-XSS-Protection "1; mode=block"

    # Static Files
    Alias /static /path/to/your/project/staticfiles
    <Directory /path/to/your/project/staticfiles>
        Require all granted
    </Directory>

    # Media Files
    Alias /media /path/to/your/project/media
    <Directory /path/to/your/project/media>
        Require all granted
    </Directory>

    # Django Application
    WSGIDaemonProcess libraryproject python-home=/path/to/venv python-path=/path/to/project
    WSGIProcessGroup libraryproject
    WSGIScriptAlias / /path/to/project/LibraryProject/wsgi.py

    <Directory /path/to/project/LibraryProject>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>
</VirtualHost>
```

Enable modules and site:
```bash
sudo a2enmod ssl
sudo a2enmod headers
sudo a2enmod rewrite
sudo a2ensite libraryproject
sudo systemctl restart apache2
```

## Step 4: Update Django for Proxy Headers

If using a reverse proxy (Nginx/Apache), update `settings.py`:

```python
# Trust proxy headers (if behind reverse proxy)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Use X-Forwarded-Host header
USE_X_FORWARDED_HOST = True
```

## Step 5: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

## Step 6: Run Security Checks

Django provides a deployment checklist:

```bash
python manage.py check --deploy
```

This checks for:
- DEBUG mode
- Secret key security
- Allowed hosts configuration
- Security settings
- Database configuration

## Step 7: Verify HTTPS Configuration

### Manual Testing

1. **HTTP Redirect Test**:
   ```bash
   curl -I http://yourdomain.com
   # Should return 301 redirect to HTTPS
   ```

2. **HTTPS Connection Test**:
   ```bash
   curl -I https://yourdomain.com
   # Should return 200 OK with security headers
   ```

3. **SSL Certificate Test**:
   - Visit: https://www.ssllabs.com/ssltest/
   - Enter your domain
   - Check for A or A+ rating

4. **Security Headers Test**:
   - Visit: https://securityheaders.com/
   - Enter your domain
   - Check security headers score

### Automated Testing Script

Create a test script `test_https.py`:

```python
import requests
import sys

def test_https(domain):
    """Test HTTPS configuration."""
    print(f"Testing HTTPS for {domain}...")
    
    # Test HTTP redirect
    try:
        response = requests.get(f"http://{domain}", allow_redirects=False, timeout=5)
        if response.status_code == 301 or response.status_code == 308:
            print("✓ HTTP redirects to HTTPS")
        else:
            print(f"✗ HTTP does not redirect (Status: {response.status_code})")
    except Exception as e:
        print(f"✗ HTTP test failed: {e}")
    
    # Test HTTPS connection
    try:
        response = requests.get(f"https://{domain}", timeout=5, verify=True)
        if response.status_code == 200:
            print("✓ HTTPS connection successful")
        else:
            print(f"✗ HTTPS returned status: {response.status_code}")
    except requests.exceptions.SSLError as e:
        print(f"✗ SSL Error: {e}")
    except Exception as e:
        print(f"✗ HTTPS test failed: {e}")
    
    # Check security headers
    try:
        response = requests.get(f"https://{domain}", timeout=5, verify=True)
        headers = response.headers
        
        required_headers = {
            'Strict-Transport-Security': 'HSTS',
            'X-Frame-Options': 'Clickjacking protection',
            'X-Content-Type-Options': 'MIME sniffing protection',
        }
        
        for header, description in required_headers.items():
            if header in headers:
                print(f"✓ {header} present: {description}")
            else:
                print(f"✗ {header} missing: {description}")
    except Exception as e:
        print(f"✗ Header check failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        domain = sys.argv[1]
    else:
        domain = "yourdomain.com"
    test_https(domain)
```

Run: `python test_https.py yourdomain.com`

## Step 8: Monitor and Maintain

### Certificate Renewal

Let's Encrypt certificates expire every 90 days. Certbot automatically renews them, but verify:

```bash
# Check certificate expiration
sudo certbot certificates

# Test renewal
sudo certbot renew --dry-run

# Manual renewal (if needed)
sudo certbot renew
```

### Log Monitoring

Monitor web server logs for security issues:

```bash
# Nginx
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# Apache
sudo tail -f /var/log/apache2/error.log
sudo tail -f /var/log/apache2/access.log
```

### Security Updates

Regularly update:
- Django and Python packages
- Web server (Nginx/Apache)
- Operating system
- SSL/TLS libraries

## Troubleshooting

### Issue: Mixed Content Warnings

**Problem**: Browser shows mixed content warnings (HTTP resources on HTTPS page)

**Solution**: 
- Ensure all static/media files are served over HTTPS
- Update any hardcoded HTTP URLs in templates
- Use `{% load static %}` for static files

### Issue: HSTS Preload Not Working

**Problem**: Site not accepted into HSTS preload list

**Solution**:
- Ensure `SECURE_HSTS_PRELOAD = True`
- Ensure `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`
- Submit to https://hstspreload.org/
- Wait for approval (can take weeks)

### Issue: Cookies Not Secure

**Problem**: Cookies still sent over HTTP

**Solution**:
- Verify `SESSION_COOKIE_SECURE = True`
- Verify `CSRF_COOKIE_SECURE = True`
- Clear browser cookies and test again
- Check that HTTPS is properly configured

### Issue: 502 Bad Gateway

**Problem**: Nginx/Apache can't connect to Django

**Solution**:
- Check Django/WSGI server is running
- Verify proxy_pass URL is correct
- Check firewall settings
- Review server logs

## Production Checklist

Before going live, verify:

- [ ] SSL certificate installed and valid
- [ ] HTTP redirects to HTTPS
- [ ] `DEBUG = False` in settings
- [ ] `ALLOWED_HOSTS` configured
- [ ] `SECURE_SSL_REDIRECT = True`
- [ ] `SESSION_COOKIE_SECURE = True`
- [ ] `CSRF_COOKIE_SECURE = True`
- [ ] HSTS configured (if desired)
- [ ] Security headers present
- [ ] Static files collected
- [ ] Database migrations applied
- [ ] Secret key is secure (not in version control)
- [ ] Web server configured correctly
- [ ] SSL certificate auto-renewal configured
- [ ] Security tests passed
- [ ] Monitoring/logging set up

## Additional Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
- [OWASP Transport Layer Protection](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html)

## Security Review Summary

The following security measures are implemented:

1. **HTTPS Enforcement**: All HTTP traffic redirected to HTTPS
2. **Secure Cookies**: Session and CSRF cookies only sent over HTTPS
3. **HSTS**: HTTP Strict Transport Security configured
4. **Security Headers**: X-Frame-Options, X-Content-Type-Options, X-XSS-Protection
5. **SSL/TLS Configuration**: Modern, secure cipher suites
6. **Certificate Management**: Auto-renewal configured (Let's Encrypt)

These measures protect against:
- Man-in-the-middle attacks
- Cookie hijacking
- Protocol downgrade attacks
- Clickjacking
- XSS attacks
- MIME type confusion

