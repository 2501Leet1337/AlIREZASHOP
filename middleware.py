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
