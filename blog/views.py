from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import PostModel


# Create your views here.
# def home_view(request):
#     print(request)
#     print(dir(request)) # all props of an instance including those indicated in dict 
#     print(request.get_full_path())
#     print(request.is_ajax())
#     return HttpResponse('<h1>This is the Blog Home Page</h1>')

def home_view(request):
    response = HttpResponse(content_type='application/json')
    # response = HttpResponse(content_type='text/html')
    # response.write('<p>This is some text...</p>')
    response.content = '<!DOCTYPE html><html><head></head><body><h1>This is some text...</h1></body>'
    response.status_code = 200
    return response

def redirect_view(request):
    return HttpResponseRedirect('/blog/some/path/') # complete url path

def post_detail_view(request, **kwargs):

    # try: 
    #     obj = PostModel.objects.get(id=1)
    # except:
    #     raise Http404

    # qs = PostModel.objects.filter(id=1)
    # obj = None
    # if not qs.exists() and qs.count() != 1:
    #     raise Http404
    # else:
    #     obj = qs.first()

    obj = get_object_or_404(PostModel, id=kwargs.get('pk'))
    context = {
        'object': obj
    }
    template = 'blog/detail_view.html'
    return render(request, template, context)

@login_required(login_url='/login/')
def post_list_view(request):
    qs = PostModel.objects.all()
    print(qs)
    # return HttpResponse('this is the queryset')
    context = {
        'object_list': qs
    }
    if request.user.is_authenticated:
        template = 'blog/list_view.html'
        context = {
            'object_list': qs,
        }
    else:
        template = 'blog/list_view_public.html'
        raise Http404
    return render(request, template, context)