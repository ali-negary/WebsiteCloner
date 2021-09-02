from django.shortcuts import render


def home(request):
    return render(request, 'myApp/base.html')


def new_search():
    pass
