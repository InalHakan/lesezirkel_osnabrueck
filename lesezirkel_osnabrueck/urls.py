"""
URL configuration for lesezirkel_osnabrueck project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.cache import never_cache

# Admin logout view that properly clears session
@never_cache
def admin_logout_view(request):
    """Custom logout view for admin that properly clears session and cookies"""
    # Clear session data
    if hasattr(request, 'session'):
        request.session.flush()
    
    # Perform logout
    logout(request)
    
    # Create response - redirect to homepage
    response = redirect('/')
    
    # Clear all authentication cookies
    response.delete_cookie('sessionid')
    response.delete_cookie('lesezirkel_sessionid')
    response.delete_cookie('csrftoken')
    response.delete_cookie('lesezirkel_csrftoken')
    
    # Add cache control headers
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response

# Ana URL yapısı (çok dilli sistem kaldırıldı)
urlpatterns = [
    path('admin/logout/', admin_logout_view, name='admin_logout'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('main.urls')),
]

# Geliştirme ortamında medya dosyalarını servis et
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
