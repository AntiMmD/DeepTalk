from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Post
from django.urls import reverse
from django.contrib.auth import get_user_model, login, authenticate
from .forms import SignUpForm
from django.core.paginator import Paginator
from django.contrib import messages
from Blog.settings import PAGINATE_BY
from django.contrib.auth.decorators import login_required
User = get_user_model()

def home(request):
    posts = Post.objects.select_related('user').all()
    paginator = Paginator(posts, PAGINATE_BY)
    page_number = request.GET.get("page")
    posts = paginator.get_page(page_number)
    return render(request, 'posts/home.html', context={'posts':posts})

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

def log_out(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('login')

def post_view(request, id):
    post_obj= get_object_or_404(Post, id=id)
    return render(request, 'posts/postView.html', context={'post': post_obj})

def delete_post(request, id):
    post_obj = get_object_or_404(Post, id=id)
    if request.user == post_obj.user:
        post_obj.delete()
        return redirect(reverse('posts:post_manager'))
    else:
        return render(request, 'posts/postView.html', 
                      context={'post': post_obj,
                               'error':"You can't delete someone else's post dummy!"})

def edit_post(request, id):
    post_obj = get_object_or_404(Post, id=id)

    if request.method == 'GET':
        if post_obj.user == request.user:
            return render(request, 'posts/postForm.html', context={'post': post_obj})
    
        messages.error(request, "You can't edit someone else's post dummy!")
        return redirect('posts:post_view', post_obj.id)
    
    if request.method == 'POST':
        if post_obj.user == request.user:
            post_header = request.POST['header_input']
            post_body = request.POST['body_input']
            post_obj.header= post_header
            post_obj.body= post_body
            post_obj.save()
            return redirect(reverse('posts:post_view', args=[post_obj.id]))
        
@login_required(login_url='sign_up')
def post_form(request):
    if request.method == 'POST':
        post_user = request.user
        post_header = request.POST['header_input']
        post_body = request.POST['body_input']
        post_obj = Post.objects.create(user= post_user, header= post_header, body= post_body)
        return redirect(reverse('posts:post_view', args=[post_obj.id]))

    return render(request, 'posts/postForm.html')

@login_required(login_url='login')
def post_manager(request):
        posts = Post.objects.filter(user= request.user)
        return render(request, 'posts/postManager.html', context={'posts':posts})

