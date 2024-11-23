from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView
from app_users import views 


urlpatterns = [
    # auth
    path('registration/' ,views.RegistrationView.as_view(), name='registration'),

    path('login/',LoginView.as_view(template_name ='app_users/login.html'),name='login'),
    #  path('logout/', LogoutView.as_view(), name='logout'),

    # path('account/',views.AccountView.as_view(),name='account'),
    path('account/<int:user_id>/', views.AccountView.as_view(), name='account'),
    path('logout/',views.logout_view, name='logout'),
    
    path('cart/<int:cart_id>/',views.CartView.as_view(),name='cart'),

    # path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    # path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    # path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),

    path('product-detail/<int:pk>/',views.ProductDetailView.as_view(),name='product_detail')
]   