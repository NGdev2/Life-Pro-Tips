from django.shortcuts import render
import random
from django.conf import settings

class UsernameMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        defaultName = request.COOKIES.get('defaultName')

        if not defaultName:
            try:
                username = random.choice(settings.NAMES_LIST)
            except (AttributeError, IndexError):
                username = "defaultName"

            request.defaultName = username

            response = self.get_response(request)

            response.set_cookie('defaultName', username, max_age=42)
            return response
        else:
            request.defaultName = defaultName
            return self.get_response(request)
