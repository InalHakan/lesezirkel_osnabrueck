"""
Custom middleware for Lesezirkel Osnabrück
"""
from django.utils.cache import add_never_cache_headers


class NeverCacheAuthenticatedMiddleware:
    """
    Middleware to prevent caching of pages for authenticated users.
    This ensures that when a user logs out, the browser doesn't show cached authenticated pages.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # If user is authenticated, add no-cache headers
        if request.user.is_authenticated:
            add_never_cache_headers(response)
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        
        return response


class ClearSessionOnLogoutMiddleware:
    """
    Middleware to ensure session is completely cleared on logout.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # If this is a logout request, ensure cookies are cleared
        if request.path in ['/accounts/logout/', '/admin/logout/']:
            if hasattr(response, 'delete_cookie'):
                response.delete_cookie('sessionid')
                response.delete_cookie('lesezirkel_sessionid')
                response.delete_cookie('csrftoken')
                response.delete_cookie('lesezirkel_csrftoken')
        
        return response
