from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
# def home_view(request):
#     print(request)
#     print(dir(request)) # all props of an instance including those indicated in dict 
#     print(request.get_full_path())
#     print(request.is_ajax())
#     return HttpResponse('<h1>This is the Blog Home Page</h1>')

def home_view(request):
    response = HttpResponse()
    response.write('<p>This is some text...</p>')
    response.status_code = 200
    return response

def redirect_view(request):
    return HttpResponseRedirect('/blog/some/path/') # 