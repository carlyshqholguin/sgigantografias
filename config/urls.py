# En el archivo urls.py en tu proyecto principal
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static



admin.site.site_header  =  "IMPRENTA"  
admin.site.site_title  =  "Administracion"
admin.site.index_title  =  "Servicios de Imprenta"

urlpatterns = [
    path('',include('apps.web.urls'))
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
