from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.shortcuts import redirect
from django.urls import reverse

def home(request):
    return render(request, r'posts/home.html')

def post_form(request):
    if request.method == 'POST':
        post_header = request.POST['header_input']
        post_body = request.POST['body_input']
        post_obj = Post.objects.create(header= post_header, body= post_body)
        return redirect(reverse('post_view', args=[post_obj.id]))
    
    return render(request, 'posts/postForm.html')

def post_view(request, id):
    post_obj= Post.objects.get(id=id)
    post_header = post_obj.header
    post_body = post_obj.body
    return render(request, 'posts/postView.html', context={'header':post_header, 'body':post_body})