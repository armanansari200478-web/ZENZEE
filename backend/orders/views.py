import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cart.models import Cart
from .models import Order, OrderItem
from .forms import OrderCreateForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest

try:
    import razorpay
except ImportError:  # pragma: no cover
    razorpay = None
from django.urls import reverse


def _initialize_payment_gateway(order, amount):
    """
    Initialize a Razorpay order when credentials exist.
    If keys are missing, the site falls back to demo mode so checkout stays usable.
    """
    # This helper creates a Razorpay Order using the API keys from environment
    # (loaded from .env via python-dotenv). We create a gateway order so the
    # frontend can open the Razorpay Checkout popup linked to this order id.
    payment_method = order.payment_method
    if payment_method == 'cod':
        return False, 'Cash on Delivery selected. No online payment gateway is required.'

    key_id = os.getenv('RAZORPAY_KEY_ID')
    key_secret = os.getenv('RAZORPAY_KEY_SECRET')

    if not key_id or not key_secret or razorpay is None:
        return True, 'Demo payment mode enabled. Add Razorpay keys to activate real online payments.'

    client = razorpay.Client(auth=(key_id, key_secret))
    response = client.order.create({
        'amount': int(amount * 100),
        'currency': 'INR',
        'receipt': order.order_number,
        'payment_capture': 1,
    })
    return True, response.get('id', order.order_number)


def checkout_view(request):
    """
    Checkout view to process orders from current cart.
    """
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        cart = Cart.objects.filter(session_key=request.session.session_key).first()

    if not cart or cart.items.count() == 0:
        messages.warning(request, "Your cart is empty. Add products before checking out!")
        return redirect('product_list')

    subtotal = cart.get_total_price()
    shipping_fee = 0 if subtotal > 1499 else 99
    total_amount = subtotal + shipping_fee

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.total_amount = total_amount
            order.shipping_fee = shipping_fee
            order.payment_method = form.cleaned_data['payment_method']

            # Save order first so that `order_number` is generated and available
            order.save()

            gateway_done, gateway_message = _initialize_payment_gateway(order, total_amount)
            if order.payment_method == 'cod':
                order.is_paid = False
            else:
                # For online payments, we keep is_paid False until verification succeeds
                order.is_paid = False

            # No external Checkout created here for Stripe; Razorpay flow will be used


            # Create OrderItems from CartItems
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    size=item.size,
                    price=item.product.get_effective_price(),
                    quantity=item.quantity
                )

            # Clear cart
            cart.items.all().delete()
            if order.payment_method == 'cod':
                messages.success(request, f"Order #{order.order_number} placed successfully! 🎉")
                messages.info(request, gateway_message)
                return redirect('order_detail', order_number=order.order_number)
            else:
                # Online payment path: gateway_message contains the razorpay order id or demo message
                razorpay_order_id = gateway_message if gateway_done else None
                # Pass necessary details to a payment page that will open Razorpay Checkout
                context = {
                    'order': order,
                    'amount': int(total_amount * 100),
                    'razorpay_order_id': razorpay_order_id,
                    'razorpay_key_id': os.getenv('RAZORPAY_KEY_ID'),
                }
                return render(request, 'orders/payment_page.html', context)
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'full_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
                'email': request.user.email,
                'phone': request.user.phone_number or '',
            }
        form = OrderCreateForm(initial=initial_data)

    context = {
        'cart': cart,
        'form': form,
        'subtotal': subtotal,
        'shipping_fee': shipping_fee,
        'total_amount': total_amount,
    }
    return render(request, 'orders/checkout.html', context)


@login_required(login_url='login')
def order_history_view(request):
    """
    List all orders for logged-in user.
    """
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_history.html', {'orders': orders})


def order_detail_view(request, order_number):
    """
    View details for a specific order.
    """
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, 'orders/order_detail.html', {'order': order})


@csrf_exempt
def payment_success(request):
    """
    Endpoint to verify Razorpay payment signature and mark order as paid.
    Expects POST with: razorpay_payment_id, razorpay_order_id, razorpay_signature, and our `order_number`.
    This verifies the signature using Razorpay client and saves `payment_id` on the Order.
    """
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid method')

    payload = request.POST
    payment_id = payload.get('razorpay_payment_id')
    razorpay_order_id = payload.get('razorpay_order_id')
    signature = payload.get('razorpay_signature')
    order_number = payload.get('order_number')

    if not all([payment_id, razorpay_order_id, signature, order_number]):
        return JsonResponse({'ok': False, 'error': 'Missing parameters'}, status=400)

    order = Order.objects.filter(order_number=order_number).first()
    if not order:
        return JsonResponse({'ok': False, 'error': 'Order not found'}, status=404)

    key_id = os.getenv('RAZORPAY_KEY_ID')
    key_secret = os.getenv('RAZORPAY_KEY_SECRET')
    if not key_id or not key_secret or razorpay is None:
        # Demo mode: accept any payment for testing
        order.is_paid = True
        order.payment_id = payment_id
        order.save()
        return JsonResponse({'ok': True, 'message': 'Demo mode: payment accepted'})

    client = razorpay.Client(auth=(key_id, key_secret))
    try:
        client.utility.verify_payment_signature({
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature,
        })
    except Exception as exc:
        return JsonResponse({'ok': False, 'error': str(exc)}, status=400)

    # Signature verified
    order.is_paid = True
    order.payment_id = payment_id
    order.save()
    return JsonResponse({'ok': True})
