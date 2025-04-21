from django.shortcuts import render


def index(request):
    context = {
        'page': "landing"
    }
    return render(request, "landing.html", context)