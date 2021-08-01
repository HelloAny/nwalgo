from django.http.response import HttpResponse
from django.shortcuts import render
 
def index(request):
    context = {}
    context['hello'] = 'Hello World!'
    return render(request, 'index.html', context)

def runoob(request):
    name = request.body
    print('name',name)
    return HttpResponse("菜鸟教程")