from .models import IPAddress 
from django.http import HttpResponse
class SaveIPAddressMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
    def __call__(self, request):
        
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        # return ip
        try:
            # global ip_address
            ip_address = IPAddress.objects.get(ip_address=ip)
        except IPAddress.DoesNotExist:
            ip_address = IPAddress(ip_address=ip)
            ip_address.save()
        request.user.ip_address = ip_address
        print(request)
        response = self.get_response(request)
        print(response)
        
        # Code to be executed for each request/response after
        # the view is called.
        return response