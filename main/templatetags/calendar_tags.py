from django import template
from django.templatetags.static import static
from django.conf import settings
import os
import time

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Dictionary'den key ile değer almak için filter"""
    return dictionary.get(key)

@register.simple_tag
def static_with_version(path):
    """Static dosya URL'sine version parametresi ekler"""
    static_url = static(path)
    
    # Development modunda dosya değişiklik zamanını kullan
    if settings.DEBUG:
        try:
            full_path = os.path.join(settings.BASE_DIR, 'static', path)
            if os.path.exists(full_path):
                mtime = int(os.path.getmtime(full_path))
                return f"{static_url}?v={mtime}"
        except:
            pass
    
    # Fallback olarak timestamp kullan
    return f"{static_url}?v={int(time.time())}"