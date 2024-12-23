from django.http import HttpResponse


# This is to check if the server is up and running on deploy
class HealthCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/up":
            response = HttpResponse("OK")
        else:
            response = self.get_response(request)

        return response
