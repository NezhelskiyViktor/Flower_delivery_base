from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    path('', views.deliver_view, name='deliver'),
    path('registration', views.registration_view, name='registration'),
    path('userlogin/', views.user_login, name='user_login'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
