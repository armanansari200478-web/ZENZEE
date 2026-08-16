from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product, Size
from .models import Cart, CartItem


def _get_cart(request):
    """
    Helper function to get or create cart for logged-in user or session.
    """
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


def cart_detail_view(request):
    """
    Display shopping cart contents and totals.
    """
    cart = _get_cart(request)
    subtotal = cart.get_total_price()
    shipping_fee = 0 if subtotal > 1499 or subtotal == 0 else 99
    total = subtotal + shipping_fee

    context = {
        'cart': cart,
        'subtotal': subtotal,
        'shipping_fee': shipping_fee,
        'total': total,
    }
    return render(request, 'cart/cart_detail.html', context)


def cart_add_view(request, product_id):
    """
    Add product to shopping cart.
    """
    product = get_object_or_404(Product, id=product_id)
    cart = _get_cart(request)

    size_id = request.POST.get('size_id')
    size = get_object_or_404(Size, id=size_id) if size_id else None

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product=product, size=size
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.info(request, f"Updated quantity for {product.name}.")
    else:
        messages.success(request, f"Added {product.name} to your cart!")

    return redirect('cart_detail')


def cart_remove_view(request, item_id):
    """
    Remove item from shopping cart.
    """
    cart = _get_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('cart_detail')
