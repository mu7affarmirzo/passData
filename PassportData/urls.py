from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.urls import path
from django.views.generic.base import TemplateView

urlpatterns = [
	path('admin/', admin.site.urls),
	path('api/users/', include('userpost.api.urls', 'as')),
	# path('api/account/', include('userpost.urls', 'account_api')),
]


if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)