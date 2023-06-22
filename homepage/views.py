from django.shortcuts import render


def index(request):
    return render(req uest, 'homepage/homepage.html')
