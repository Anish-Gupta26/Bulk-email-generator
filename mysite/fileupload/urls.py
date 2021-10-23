from django.urls import path
from .views import home, upload, matching, send_mail, about
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',home),
    path('about',about),
    path('upload',upload),
    path('match',matching),
    path('output',send_mail)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)