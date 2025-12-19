from django.contrib.auth import get_user_model
import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.http import require_http_methods, require_GET
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.db.models import Q
from .models import Post
User = get_user_model()

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

