from django.urls import path

from .import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.CategoriesView.as_view(),name='categories'),
    # path('product/',views.ProductiesView.as_view(),name='products'),
    path('products/<int:category_id>/', views.ProductiesView.as_view(), name='products'),

    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),


]  
if settings.DEBUG:
    urlpatterns += static(prefix = settings.MEDIA_URL, document_root =settings.MEDIA_ROOT )
    urlpatterns += static(prefix = settings.STATIC_URL, document_root =settings.STATIC_ROOT)
    