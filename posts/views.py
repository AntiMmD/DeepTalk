from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model, login, authenticate
from .forms import SignUpForm
User = get_user_model()

def home(request):
    all_the_posts_in_the_world= Post.objects.all() 
    return render(request, 'posts/home.html', context={'posts':all_the_posts_in_the_world})

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    
    return render(request, 'posts/signUp.html', context={'form': form})     

def log_in(request):
    if request.method == 'POST':
        email=request.POST['email_input']
        password= request.POST['password_input']
 
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('home'))

    return render(request, 'posts/login.html')

def post_form(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            post_user = request.user
            post_header = request.POST['header_input']
            post_body = request.POST['body_input']
            post_obj = Post.objects.create(user= post_user, header= post_header, body= post_body)
            return redirect(reverse('posts:post_view', args=[post_obj.id]))
        
        return render(request, 'posts/postForm.html')
    
    else:
        return redirect(reverse('sign_up'))

def post_view(request, id):
    post_obj= Post.objects.get(id=id)
    post_header = post_obj.header
    post_body = post_obj.body
    return render(request, 'posts/postView.html', context={'header':post_header, 'body':post_body})

def post_manager(request):
    if request.user.is_authenticated:
            posts = Post.objects.filter(user= request.user)
            return render(request, 'posts/postManager.html', context={'posts':posts})
    
    return(redirect('login'))
