from django.shortcuts import render,redirect
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth import authenticate, login,logout
from django.views.generic.edit import CreateView
from django.views.generic import ListView,DetailView,UpdateView
from django.contrib.auth.views import LoginView
from .models import UserModel
from .forms import UserRegistrationForm,AccountForm
from django.urls import reverse_lazy 
from django.shortcuts import get_object_or_404

from app_users.models import Cart, Product

from app_users.forms import UserRegistrationForm
from app_users.models import UserModel


class RegistrationView(CreateView):
    model = UserModel
    template_name = 'app_users/regstration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        return super().form_valid(form)

    
def logout_view(request):
    logout(request)
    return redirect('login')


class AccountView(CreateView):
    model = UserModel
    template_name = 'app_users/account.html'
    form_class = AccountForm
    pk_url_kwarg = 'user_id'
    success_url = reverse_lazy('login')

    def get_object(self, queryset=None):
        user_id = self.kwargs.get('user_id')

        if user_id:
            return UserModel.objects.filter(id=user_id).first()  # Fetch object by user_id
        return None


# class CartView(ListView):
#     model = Cart
#     template_name = 'app_users/cart.html'
#     context_object_name = 'cart'

#     def get_queryset(self):
#         return Cart.objects.filter(user=self.request.user)
class CartView(ListView):
    model = Cart
    template_name = 'app_users/cart.html'
    context_object_name = 'cart'

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_total'] = sum(item.product.price * item.quantity for item in self.get_queryset())
        return context

###Cart   remove add ###
def add_to_cart(request, product_id):
        product = get_object_or_404(Product, id=product_id)
        if request.method == 'POST':
         user = request.user
        quantity = int(request.POST.get('quantity', 1))

        cart_item, created = Cart.objects.get_or_create(product=product, user=product_id)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        return redirect('product_detail', product_id=product.id)


# def remove_from_cart(request, item_id):
#     cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
#     cart_item.delete()
#     return redirect('view_cart')

# def update_cart(request, item_id):
#     cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
#     if request.method == 'POST':
#         quantity = int(request.POST.get('quantity', 1))
#         if quantity > 0:
#             cart_item.quantity = quantity
#             cart_item.save()
#         else:
#             cart_item.delete()  # Remove item if quantity is set to 0
#     return redirect('cart')

# def view_cart(request):
#     cart_items = Cart.objects.filter(user=request.user)
#     cart_total = sum(item.product.price * item.quantity for item in cart_items)
#     return render(request, 'cart.html', {
#         'cart': cart_items,
#         'cart_total': cart_total,
#     })








def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        comment = request.POST.get('comment')
        
        if len(comment.strip()) >= 10:
            new_comment = Product.objects.create(
                owner=request.user,
                product=product,
                body=comment
            )
            new_comment.save()
            return redirect(f'/cart/{product_id}#comments-section')

    context = {
        'product': product,

    }

    extra_context = {
        'footer_fixed': True,
    }
    return render(request, 'app_users/cart.html', context)




class ProductDetailView(DetailView):
    model =Product
    template_name = 'app_users/detail.html'
    context_object_name = 'product'
    success_url = reverse_lazy('cart')