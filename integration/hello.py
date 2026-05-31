from django.http import HttpResponse


def greet(request):
    return HttpResponse("ackhava.dev CI/CD, version 2")
