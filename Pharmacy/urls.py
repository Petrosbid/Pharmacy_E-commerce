from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "پنل مدیریت من"
admin.site.site_title = "مدیریت سایت"
admin.site.index_title = "به داشبورد مدیریت خوش آمدید"

urlpatterns = [
    path('dashboard/', include('admin_material.urls')),
    path('admin/', admin.site.urls),

    path('', include('core.urls')),
    path('users/', include('users.urls')),
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
    path('cart/', include('cart.urls')),
    path('payment/', include('payment.urls')),
    path('prescriptions/', include('prescriptions.urls')),
    path('blog/', include('blog.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


