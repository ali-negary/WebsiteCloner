from django.shortcuts import render


def home(request):
    return render(request, 'base.html')


def new_search(request):
    # this .get in search is not HTTP GET/POST methods. it is because result of request.POST is dictionary.
    search = request.POST.get('search')
    material_for_front = {
        'search': search,
    }
    return render(request, 'myApp/new_search.html', material_for_front)
