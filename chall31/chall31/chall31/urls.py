from django.contrib import admin
from django.urls import include, path
urlpatterns = [
    path('vulnApp/', include('vulnApp.urls')),
    path('admin/', admin.site.urls),
]
