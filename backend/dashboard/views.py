from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count
from django.contrib.auth import get_user_model
from products.models import Product, Category
from orders.models import Order

User = get_user_model()


@staff_member_required(login_url='login')
def admin_dashboard_view(request):
    """
    Staff / Admin Dashboard view showing platform metrics, sales stats, and order management.
    """
    total_users = User.objects.count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    recent_orders = Order.objects.all()[:10]

    context = {
        'total_users': total_users,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)
