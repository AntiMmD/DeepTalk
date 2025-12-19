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
from django.views.decorators.http import require_GET,require_POST, require_http_methods
from django.http import JsonResponse
User = get_user_model()

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


@login_required(login_url='login')
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


@login_required(login_url='login')
@require_POST
def delete_post(request, id):
    post_obj = get_object_or_404(Post, id=id)
    if request.user == post_obj.user:
        post_obj.delete()
        return redirect(reverse('posts:post_manager'))
    else:
        messages.error(request, "You can't delete someone else's post dummy!")
        return render(request, 'posts/postView.html', 
                      context={'post': post_obj}, status=403)


@login_required(login_url='login')
@require_http_methods(['GET','POST'])
def edit_post(request, id):
    post_obj = get_object_or_404(Post, id=id)
    
    if post_obj.user != request.user:
        messages.error(request, "You can't edit someone else's post dummy!")
        return render(request, 'posts/postView.html', 
                      context={'post': post_obj}, status=403)
    
    if request.method == 'GET':
        return render(request, 'posts/postForm.html', context={'post': post_obj})
    
    if request.method == 'POST':
        post_header = request.POST['header_input']
        post_body = request.POST['body_input']
        post_obj.header= post_header
        post_obj.body= post_body
        post_obj.save()
        return redirect(reverse('posts:post_view', args=[post_obj.id]))
    


@require_GET
def posts_api_list(request):
    """
    Return a JSON list of posts for the frontend SPA to consume.
    """
    qs = Post.objects.select_related('user').all()
    posts = []
    for p in qs:
        posts.append({
            "id": p.id,
            "header": p.header,
            "body": p.body,
            "user": p.user.username,
            "created_at": p.created_at.isoformat() if p.created_at else None,
        })
    return JsonResponse({"posts": posts})


# Add these imports near the top of the file if they are not already present
import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.http import require_http_methods, require_GET
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.db.models import Q

# CSRF token view (call this first from the client to ensure cookie is set)
@require_GET
def csrf_token_view(request):
    """
    Return a JSON object with a CSRF token and ensure the cookie is set.
    Client should call GET /posts/api/csrf/ before posting forms.
    """
    token = get_token(request)
    return JsonResponse({"csrfToken": token})


# AUTH APIs: login, signup, logout
@require_http_methods(["POST"])
def api_login(request):
    try:
        data = json.loads(request.body.decode())
    except Exception:
        return HttpResponseBadRequest("Invalid JSON")
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return JsonResponse({"error": "Missing email or password"}, status=400)

    user = authenticate(request, username=email, password=password)
    if user is None:
        return JsonResponse({"error": "Invalid credentials"}, status=400)

    auth_login(request, user)
    return JsonResponse({"ok": True, "user": {"email": user.email, "username": user.username}})


@require_http_methods(["POST"])
def api_signup(request):
    """
    Minimal signup API: creates a user with (username, email, password).
    NOTE: This does NOT require captcha — add it later if you need.
    """
    try:
        data = json.loads(request.body.decode())
    except Exception:
        return HttpResponseBadRequest("Invalid JSON")
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    if not (email and username and password):
        return JsonResponse({"error": "email, username and password are required"}, status=400)

    # Basic uniqueness checks (same logic as your SignUpForm)
    existing = User.objects.filter(Q(email=email) | Q(username=username)).first()
    if existing:
        errs = {}
        if existing.email == email:
            errs["email"] = "A user with this email already exists"
        if existing.username == username:
            errs["username"] = "This username is taken"
        return JsonResponse({"errors": errs}, status=400)

    # create user and log in
    user = User.objects.create_user(username=username, email=email, password=password)
    auth_login(request, user)
    return JsonResponse({"ok": True, "user": {"email": user.email, "username": user.username}})


@require_http_methods(["POST"])
def api_logout(request):
    auth_logout(request)
    return JsonResponse({"ok": True})


# POSTS API: create / edit / delete (read is already implemented)
@require_http_methods(["POST"])
def posts_api_create(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)
    try:
        data = json.loads(request.body.decode())
    except Exception:
        return HttpResponseBadRequest("Invalid JSON")
    header = data.get("header", "")
    body = data.get("body", "")
    post_obj = Post.objects.create(user=request.user, header=header, body=body)
    return JsonResponse({
        "post": {
            "id": post_obj.id,
            "header": post_obj.header,
            "body": post_obj.body,
            "user": post_obj.user.username,
            "created_at": post_obj.created_at.isoformat() if post_obj.created_at else None,
        }
    })


@require_http_methods(["POST"])
def posts_api_edit(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)
    try:
        post_obj = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)

    if post_obj.user != request.user:
        return JsonResponse({"error": "Permission denied"}, status=403)

    try:
        data = json.loads(request.body.decode())
    except Exception:
        return HttpResponseBadRequest("Invalid JSON")
    post_obj.header = data.get("header", post_obj.header)
    post_obj.body = data.get("body", post_obj.body)
    post_obj.save()
    return JsonResponse({"ok": True, "post": {
        "id": post_obj.id,
        "header": post_obj.header,
        "body": post_obj.body,
        "user": post_obj.user.username,
        "created_at": post_obj.created_at.isoformat() if post_obj.created_at else None,
    }})


@require_http_methods(["POST"])
def posts_api_delete(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)
    try:
        post_obj = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)
    if post_obj.user != request.user:
        return JsonResponse({"error": "Permission denied"}, status=403)
    post_obj.delete()
    return JsonResponse({"ok": True})

