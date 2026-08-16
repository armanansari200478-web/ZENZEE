from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import Review


@login_required(login_url='login')
def add_review_view(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        rating = int(request.POST.get('rating', 5))
        comment = request.POST.get('comment', '').strip()

        if comment:
            Review.objects.create(
                product=product,
                user=request.user,
                rating=min(max(rating, 1), 5),
                comment=comment
            )
            messages.success(request, "Thank you for your product review!")
        else:
            messages.error(request, "Please enter a comment before submitting.")

    return redirect('product_detail', slug=product.slug)
