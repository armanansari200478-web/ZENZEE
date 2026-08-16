from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import Wishlist


@login_required(login_url='login')
def wishlist_view(request):
    items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist/wishlist.html', {'items': items})


@login_required(login_url='login')
def wishlist_toggle_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wish_item = Wishlist.objects.filter(user=request.user, product=product).first()

    if wish_item:
        wish_item.delete()
        messages.info(request, f"Removed {product.name} from your wishlist.")
    else:
        Wishlist.objects.create(user=request.user, product=product)
        messages.success(request, f"Saved {product.name} to your wishlist! ❤️")

    return redirect(request.META.get('HTTP_REFERER', 'product_list'))
