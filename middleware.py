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

        # Remove requests older than 60 seconds
        now = time()
        requests = [req for req in requests if now - req < 60]
        requests.append(now)

        # Save updated request times to cache
        cache.set(key, requests, timeout=60)

        # If there are more than 10 requests in the past minute, block
        if len(requests) > 10:
            return HttpResponseForbidden("Too many requests. Try again later.")

        return self.get_response(request)

    def get_client_ip(self, request):
        """Retrieve client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip