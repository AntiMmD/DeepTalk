from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Post
from django.urls import reverse
from django.contrib.auth import get_user_model, login
from .forms import SignUpForm, LoginForm
from django.core.paginator import Paginator
from django.contrib import messages
from Blog.settings import PAGINATE_BY
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET,require_POST, require_http_methods
User = get_user_model()

@csrf_exempt
@require_GET
def home(request):
    posts = Post.objects.select_related('user').all()
    paginator = Paginator(posts, PAGINATE_BY)
    page_number = request.GET.get("page")
    posts = paginator.get_page(page_number)
    return render(request, 'posts/home.html', context={'posts':posts})


@require_http_methods(["GET", "POST"])
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


@require_http_methods(["GET", "POST"])
def log_in(request):
    if request.method == 'POST':
        form= LoginForm(request.POST)
        if form.is_valid():
            login(request, form.cleaned_data['user'])
            return redirect(reverse('home'))
        else: 
            return render(request, 'posts/login.html', context={'form': form})

    elif request.method == 'GET':
        return render(request, 'posts/login.html', context={'form': LoginForm()})

def log_out(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('login')

@login_required(login_url='sign_up')
@require_http_methods(["GET", "POST"])
def create_post(request):
    if request.method == 'POST':
        post_user = request.user
        post_header = request.POST['header_input']
        post_body = request.POST['body_input']
        post_obj = Post.objects.create(user= post_user, header= post_header, body= post_body)
        return redirect(reverse('posts:post_view', args=[post_obj.id]))

    return render(request, 'posts/postForm.html')


@login_required(login_url='login')
@require_GET
def post_manager(request):
        posts = Post.objects.filter(user= request.user)
        return render(request, 'posts/postManager.html', context={'posts':posts})


@require_GET
def post_view(request, id):
    post_obj= get_object_or_404(Post, id=id)
    return render(request, 'posts/postView.html', context={'post': post_obj})


@require_POST
@login_required(login_url='login')
def delete_post(request, id):
    post_obj = get_object_or_404(Post, id=id)
    if request.user == post_obj.user:
        post_obj.delete()
        return redirect(reverse('posts:post_manager'))
    else:
        return render(request, 'posts/postView.html', 
                      context={'post': post_obj,
                               'error':"You can't delete someone else's post dummy!"})


@require_http_methods(['GET','POST'])
@login_required(login_url='login')
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

