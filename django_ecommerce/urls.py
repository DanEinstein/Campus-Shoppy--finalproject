"""django_ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from . import views
from .health import health_check


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('home/', views.home_view, name='home'),
    path('health/', health_check, name='health'),
    path('blog/', include('blog.urls')),
    path('contact/', include('contact.urls')),
    path('about/', include('about.urls')),
    path('shop/', include('shop.urls')),
    path('cart/', include('cart.urls')),
    path('payments/', include('payments.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('account/', include('account.urls')),
    # Handle Chrome DevTools well-known probe to reduce 404 noise
    path('.well-known/appspecific/com.chrome.devtools.json', lambda request: HttpResponse(status=204)),
    # Handle favicon requests
    path('favicon.ico', lambda request: HttpResponse(status=204)),
]

# Gracefully handle accidental paste of terminal hint (leading space becomes %20)
# Use re_path to allow whitespace in the matched URL.
urlpatterns += [
    re_path(r"^\sQuit\s+the\s+server\s+with\s+CTRL\-BREAK\.$", RedirectView.as_view(url='/', permanent=False)),
]

# Serve media files in production
if not settings.DEBUG:
    urlpatterns += [
        path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
    ]

# Serve static and media files in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)