from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import get_user_model, login


def home(request):
    return render(request, r'posts/home.html')

User = get_user_model()
def sign_up(request):
    if request.method == 'POST':
        email = request.POST['email_input']
        username= request.POST['username_input']
        password = request.POST['password_input']
        user = User.objects.create_user(email=email,username=username, password=password)
        login(request, user)  
        return redirect('home')
    
    return render(request, 'posts/signUp.html')


def post_form(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            post_user = request.user
            post_header = request.POST['header_input']
            post_body = request.POST['body_input']
            post_obj = Post.objects.create(user= post_user, header= post_header, body= post_body)
            return redirect(reverse('post_view', args=[post_obj.id]))
        
        return render(request, 'posts/postForm.html')
    
    else:
        return redirect(reverse('sign_up'))

def post_view(request, id):
    post_obj= Post.objects.get(id=id)
    post_header = post_obj.header
    post_body = post_obj.body
    return render(request, 'posts/postView.html', context={'header':post_header, 'body':post_body})

def post_manager(request):
    
    posts = Post.objects.all()
    return render(request, 'posts/postManager.html', context={'posts':posts})
