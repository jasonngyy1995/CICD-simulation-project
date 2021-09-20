from django.http import HttpResponse

def home(request):
    return HttpResponse("Testing Home page")