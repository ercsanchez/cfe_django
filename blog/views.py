from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404

from .models import Post
from .forms import PostForm



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


@login_required
def post_create_view(request):
    # if request.method == 'POST':
    #     print('request.POST:', request.POST)
    #     form = PostForm(request.POST)
    #     if form.is_valid():
    #         form.save(commit=False)
    #         print('form.cleaned_data:', form.cleaned_data)

    form = PostForm(request.POST or None)
    template = 'blog/create_view.html'
    context = {
        'form': form
    }

    if form.is_valid():
        obj = form.save(commit=False) # only req'd. if using ModelForm
        print('obj.title:', obj.title)
        obj.save()
        messages.success(request, 'Created a New Blog Post')
        # if you want to display a new form after creating a new post
        # context = {
        #     'form': PostForm()
        # }
        return HttpResponseRedirect(f'/blog/{obj.id}/')

    return render(request, template, context)


@login_required
def post_update_view(request, **kwargs):
    obj = get_object_or_404(Post, id=kwargs.get('pk'))
    template = 'blog/update_view.html'
    form = PostForm(request.POST or None, instance=obj)
    context = {
        # 'object': obj,
        'form': form,
    }

    if form.is_valid():
        form.save()
        messages.success(request, 'Updated the Blog Post')
        return HttpResponseRedirect(f'/blog/{obj.id}/')

    return render(request, template, context)


def post_delete_view(request, pk=None):
    obj = get_object_or_404(Post, id=pk)
    template = 'blog/delete_view.html'

    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Post deleted')
        return HttpResponseRedirect('/blog/posts/')
    context = {
        'object': obj,
    }
    return render(request, template, context)

def post_detail_view(request, pk=None):

    # try: 
    #     obj = Post.objects.get(id=1)
    # except:
    #     raise Http404

    # qs = Post.objects.filter(id=1)
    # obj = None
    # if not qs.exists() and qs.count() != 1:
    #     raise Http404
    # else:
    #     obj = qs.first()

    obj = get_object_or_404(Post, id=pk)
    context = {
        'object': obj
    }
    template = 'blog/detail_view.html'
    return render(request, template, context)


@login_required(login_url='/login/')
def post_list_view(request):
    qs = Post.objects.all()
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


# combining all crud views
def post_robust_view(request, pk=None):
    obj = None
    context = {}
    success_message = 'Created a new blog post'
    template = 'blog/detail_view.html'

    if pk is None:
        'obj could be created'
        template = 'blog/create_view.html'

    else:
        'obj probably exists'
        obj = get_object_or_404(Post, id=pk)
        success_message = 'Updated a new blog post'
        context['object'] = obj

        if 'update' in request.get_full_path():
            template = 'blog/update_view.html'

        if 'delete' in request.get_full_path():
            template = 'blog/delete_view.html'
            if request.method == 'POST':
                obj.delete()
                messages.success(request, 'Post deleted')
                return HttpResponseRedirect('/blog/posts/')

    # if 'update' in request.get_full_path() or 'create' in request.get_full_path():
    form = PostForm(request.POST or None, instance=obj)
    context['form'] = form
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, success_message)
        if obj is not None:
            return HttpResponseRedirect('/blog/{obj.id}/')
        context['form'] = PostForm()

    return render(request, template, context)