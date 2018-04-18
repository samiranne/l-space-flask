from django.http import HttpResponse

def get_books(request):
    return HttpResponse("Hello world!")
