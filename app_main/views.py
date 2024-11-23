from django.shortcuts import render,redirect
from django.views.generic import ListView
from django.db.models import Q
from .models import Product,Categories
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from app_users.models import Cart
# Create your views here.

class CustomRangeForPagination:
        
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)

    
        paginator = context['paginator']
        page_obj = context ['page_obj']
        left_index = page_obj.number - 1
        right_index = page_obj.number + 1

        if left_index < 1:
            left_index = 1

        if right_index >  page_obj.paginator.num_pages:
            right_index = page_obj.paginator.num_pages


        custom_range  = range(left_index,right_index +1)
        context['custom_range'] = custom_range




        return context
    
class CategoriesView(CustomRangeForPagination,ListView):
    model = Categories
    template_name = 'app_main/categories.html'
    context_object_name = 'categories' 
    paginator_class = Paginator
    paginate_by = 1


    def get_queryset(self):
        search_term = self.request.GET.get('q', '')  # Get the search query from the GET parameters
        if search_term:
            # Search for categories whose title contains the search term (case-insensitive)
            return Categories.objects.filter(
                Q(title__icontains=search_term)
            )
        else:
            return Categories.objects.all() 


class ProductiesView(ListView):
    template_name = "app_main/index.html"
    context_object_name = 'products'
    paginator_class = Paginator
    paginate_by = 1

    def get_queryset(self):
        return Product.objects.filter(category__id=self.kwargs.get("category_id"))
    


    def get_queryset(self):
  
        category_id = self.kwargs.get("category_id")

        search_term = self.request.GET.get('q', '')  

        queryset = Product.objects.filter(category__id=category_id)

        if search_term:
            queryset = queryset.filter(
                Q(title__icontains=search_term) | 
                Q(description__icontains=search_term) 
            )

        return queryset
    
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

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('view_cart')

def update_cart(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()  # Remove item if quantity is set to 0
    return redirect('cart')

def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    cart_total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {
        'cart': cart_items,
        'cart_total': cart_total,
    })
