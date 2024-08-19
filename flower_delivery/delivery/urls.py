from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    path('', views.deliver_view, name='deliver'),
    path('registration', views.registration_view, name='registration'),
    path('entrance', views.entrance_view, name='entrance'),
    path('viewsrec', views.viewsrec_view, name='viewsrec'),
    path('exit', views.exit_view, name='exit'),
    path('catalog', views.catalog_view, name='catalog'),
    path('order', views.order_view, name='order'),
]  # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
