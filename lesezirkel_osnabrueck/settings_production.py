import os
from pathlib import Path
from .settings import *

# Environment variables kullanımı için
try:
    from decouple import config
    USE_DECOUPLE = True
except ImportError:
    USE_DECOUPLE = False
    config = lambda key, default='': os.environ.get(key, default)

# SECURITY WARNING: keep the secret key used in production secret!
if USE_DECOUPLE:
    SECRET_KEY = config('DJANGO_SECRET_KEY')
else:
    SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'your-secret-key-here-CHANGE-THIS')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'lesezirkel-os.de',
    'www.lesezirkel-os.de',
    '95.216.100.62',
    'veraxic.com',
    'localhost',
    '127.0.0.1',
]

# Database for production
# SQLite kullanıyoruz (basit, dosya tabanlı, kurulum gerektirmez)
DB_ENGINE = os.environ.get('DB_ENGINE', 'sqlite')

if DB_ENGINE == 'sqlite':
    # SQLite - Basit ve hızlı kurulum
    # Veritabanını ayrı bir klasörde sakla (izin sorunlarını önlemek için)
    DB_DIR = os.path.join(BASE_DIR, 'db')
    if not os.path.exists(DB_DIR):
        try:
            os.makedirs(DB_DIR, mode=0o775)
        except OSError:
            pass
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(DB_DIR, 'lesezirkel_osnabrueck.sqlite3'),
        }
    }
elif DB_ENGINE == 'mysql':
    # MySQL/MariaDB (ileride geçmek isterseniz)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('DB_NAME', 'db_name'),
            'USER': os.environ.get('DB_USER', 'db_user'),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '3306'),
            'OPTIONS': {
                'charset': 'utf8mb4',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }
elif DB_ENGINE == 'postgresql':
    # PostgreSQL (alternatif)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME', 'db_name'),
            'USER': os.environ.get('DB_USER', 'db_user'),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '5432'),
        }
    }

# Static files for production - All-Inkl
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Media files for production - All-Inkl
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# WhiteNoise settings for static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 86400
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# HTTPS settings (if using HTTPS)
SECURE_SSL_REDIRECT = True  # HTTPS yönlendirmesi
SESSION_COOKIE_SECURE = True  # Session cookie'lerini güvenli yap
CSRF_COOKIE_SECURE = True  # CSRF cookie'lerini güvenli yap
SESSION_COOKIE_HTTPONLY = True  # JavaScript erişimini engelle
CSRF_COOKIE_HTTPONLY = True  # JavaScript erişimini engelle
SESSION_COOKIE_SAMESITE = 'Strict'  # CSRF koruması
CSRF_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_NAME = 'lesezirkel_sessionid'  # Özel session cookie adı
CSRF_COOKIE_NAME = 'lesezirkel_csrftoken'  # Özel CSRF cookie adı

# Session Configuration
SESSION_COOKIE_AGE = 3600  # 1 saat
SESSION_SAVE_EVERY_REQUEST = True  # Her istekte session'ı güncelle
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Tarayıcı kapanınca session sona ersin

# Cache Control - Authenticated sayfaların cache'lenmesini engelle
CACHE_MIDDLEWARE_SECONDS = 0
CACHE_MIDDLEWARE_KEY_PREFIX = ''

# File Upload Settings - settings.py ile aynı
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10 MB

# Logging - All-Inkl uyumlu
# Logs klasörünün varlığını kontrol et ve oluştur
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
LOGS_AVAILABLE = False

try:
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR, mode=0o775)
    # Test yazma izni
    test_file = os.path.join(LOGS_DIR, '.write_test')
    with open(test_file, 'w') as f:
        f.write('test')
    os.remove(test_file)
    LOGS_AVAILABLE = True
except (OSError, PermissionError):
    # Log dosyaları kullanılamıyorsa sadece console kullan
    LOGS_AVAILABLE = False

# Logging yapılandırması
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'main': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Eğer log dosyaları yazılabilirse ekle
if LOGS_AVAILABLE:
    LOGGING['handlers']['file'] = {
        'level': 'INFO',
        'class': 'logging.FileHandler',
        'filename': os.path.join(LOGS_DIR, 'production.log'),
        'formatter': 'verbose',
    }
    LOGGING['handlers']['error_file'] = {
        'level': 'ERROR',
        'class': 'logging.FileHandler',
        'filename': os.path.join(LOGS_DIR, 'error.log'),
        'formatter': 'verbose',
    }
    LOGGING['loggers']['django']['handlers'].extend(['file', 'error_file'])
    LOGGING['loggers']['main']['handlers'].extend(['file', 'error_file'])

# Email ayarları (hata bildirimleri için)
ADMINS = [('Admin', 'info@lesezirkel-os.de')]
SERVER_EMAIL = 'noreply@lesezirkel-os.de'

# All-Inkl SMTP ayarları (gerekirse)
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.all-inkl.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = os.environ.get('EMAIL_USER', '')
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD', '')

# Authentication settings
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/events/'
LOGOUT_REDIRECT_URL = '/'

# Django Messages Framework - Bootstrap 5 compatibility
from django.contrib.messages import constants as message_constants
MESSAGE_TAGS = {
    message_constants.DEBUG: 'secondary',
    message_constants.INFO: 'info',
    message_constants.SUCCESS: 'success',
    message_constants.WARNING: 'warning',
    message_constants.ERROR: 'danger',  # Bootstrap uses 'danger' for error (red)
}

# Jazzmin Admin Theme Configuration
JAZZMIN_SETTINGS = {
    # Title on the login screen and header
    "site_title": "Lesezirkel Admin",
    "site_header": "Lesezirkel",
    "site_brand": "Lesezirkel",
    
    # Logo to use for your site (path relative to STATIC_URL)
    "site_logo": "images/logo.png",
    "login_logo": "images/logo.png",
    
    # Logo to use for login form in dark themes
    "login_logo_dark": None,
    
    # CSS classes to add to site logo
    "site_logo_classes": "img-circle",
    
    # Relative path to a favicon
    "site_icon": None,
    
    # Welcome text on the login screen
    "welcome_sign": "Willkommen im Admin-Bereich",
    
    # Copyright on the footer
    "copyright": "Lesezirkel Osnabrück e.V. 2025",
    
    # The model admin to search from the search bar
    "search_model": ["auth.User", "main.Event", "main.News"],
    
    # Field name on user model that contains avatar image
    "user_avatar": None,
    
    ############
    # Top Menu #
    ############
    
    # Links to put along the top menu
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Website", "url": "/", "new_window": True},
        {"model": "auth.User"},
        {"app": "main"},
    ],
    
    #############
    # Side Menu #
    #############
    
    # Whether to display the side menu
    "show_sidebar": True,
    
    # Whether to aut expand the menu
    "navigation_expanded": True,
    
    # Custom icons for side menu apps/models
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "main.Event": "fas fa-calendar-alt",
        "main.News": "fas fa-newspaper",
        "main.TeamMember": "fas fa-user-tie",
        "main.Gallery": "fas fa-images",
        "main.Contact": "fas fa-envelope",
        "main.EventRegistration": "fas fa-user-check",
        "main.Document": "fas fa-file-alt",
        "main.Certificate": "fas fa-certificate",
    },
    
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    
    #################
    # Related Modal #
    #################
    "related_modal_active": False,
    
    #############
    # UI Tweaks #
    #############
    
    # Render out the change view as a single form, or in tabs
    "changeform_format": "horizontal_tabs",
    
    # Override change forms on a per modeladmin basis
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
}

# Jazzmin UI Tweaks
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-primary",
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_nav_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}