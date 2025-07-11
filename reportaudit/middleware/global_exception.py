import traceback
from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin

class GlobalExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        # Log the exception (or send an email, etc.)
        print("Exception caught by middleware:", exception)
        traceback.print_exc()

        return render(request, r'templates\\error\\500.html', status=500)
