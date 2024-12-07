from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import product_list, product_detail, approve_comment

urlpatterns = [
    path('products/', product_list, name='product_list'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('approve_comment/<int:comment_id>/', approve_comment, name='approve_comment'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
