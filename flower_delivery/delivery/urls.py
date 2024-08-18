from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    path('', views.deliver_view, name='deliver'),
    path('registration', views.registration_view, name='registration'),
    path('login', views.login_view, name='login'),
    path('viewsrec', views.viewsrec_view, name='viewsrec'),
]  # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
