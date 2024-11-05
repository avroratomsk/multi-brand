from django.urls import path,include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from .sitemap import PostSitemap, ShopCategory, ShopProduct

sitemaps = {
    'posts': PostSitemap,
    'category': ShopCategory,
    'products': ShopProduct,
}

from main import settings

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('about/', include('home.urls')),
    path('category/', include('shop.urls')),
    path('blog/', include('blog.urls')),
    path('service/', include('service.urls')),
    path('user/', include('users.urls')),
    path('reviews/', include('reviews.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('order.urls')),
    path('admin/', include('admin.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),  # Маршрут для sitemap.xml
    path('', include('home.urls')),
]


if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
    
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)