from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category, Brand, Size


def product_list_view(request):
    """
    Displays all available products with filtering by category, brand, and sorting.
    """
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.filter(is_active=True)
    brands = Brand.objects.all()

    # Category Filter
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    # Search Query
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(category__name__icontains=query)
        )

    # Sort By
    sort = request.GET.get('sort')
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created_at')

    context = {
        'products': products,
        'categories': categories,
        'brands': brands,
        'selected_category': category_slug,
        'search_query': query,
    }
    return render(request, 'products/product_list.html', context)


def product_detail_view(request, slug):
    """
    Detailed page for a single product with image gallery, size selector, and reviews.
    """
    product = get_object_or_404(Product, slug=slug, is_available=True)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)
