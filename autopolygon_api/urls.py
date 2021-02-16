from django.contrib import admin
from django.urls import path, include, re_path
import debug_toolbar
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
