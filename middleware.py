# Alirezashop/middleware.py
from time import time
from django.core.cache import cache
from django.http import HttpResponseForbidden

class ThrottleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_client_ip(request)
        endpoint = request.path
        key = f"throttle-{ip}-{endpoint}"
        requests = cache.get(key, [])

        
        now = time()
        requests = [req for req in requests if now - req < 80]
        requests.append(now)

        
        cache.set(key, requests, timeout=60)

        
        if len(requests) > 10:
            return HttpResponseForbidden("Request overload Please Try again later.")

        return self.get_response(request)

    def get_client_ip(self, request):
        
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class InputNormalizationMiddleware:
   

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
       
        request.GET = self._normalize_querydict(request.GET)
        request.POST = self._normalize_querydict(request.POST)
        return self.get_response(request)

    def _normalize_querydict(self, querydict):
        
        normalized = querydict.copy()
        for key, value in normalized.lists():
            normalized.setlist(
                key, 
                [v.strip() if isinstance(v, str) else v for v in value]
            )
        return normalized   