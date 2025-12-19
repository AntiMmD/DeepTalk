from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),

    # Keep the posts app (it contains our API endpoints at /posts/api/...)
    path("posts/", include("posts.urls", namespace="posts")),

    # Keep captcha URLs if you use them
    path("captcha/", include("captcha.urls")),
]

if not settings.TESTING:
    from debug_toolbar.toolbar import debug_toolbar_urls
    urlpatterns += debug_toolbar_urls()

# SPA fallback: serve index.html for any non-admin/non-static/non-api route.
# Note: we exclude admin, static, posts (where APIs live), captcha.
urlpatterns += [
    re_path(
        r"^(?!admin/|static/|posts/|captcha/).*$",
        TemplateView.as_view(template_name="index.html"),
    ),
]
