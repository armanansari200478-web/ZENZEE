from django.core.management.base import BaseCommand
from products.models import Category, Brand, Size, Product, ProductSize


class Command(BaseCommand):
    help = "Seeds initial ZENZEE youth fashion categories, brands, sizes, and products."

    def handle(self, *args, **options):
        self.stdout.write("Seeding ZENZEE platform data...")

        # Categories
        cat_streetwear, _ = Category.objects.get_or_create(
            name="Streetwear", description="Urban Gen-Z streetwear collection."
        )
        cat_oversized, _ = Category.objects.get_or_create(
            name="Oversized", description="Heavyweight oversized hoodies and relaxed fit tees."
        )
        cat_cargo, _ = Category.objects.get_or_create(
            name="Cargo Pants", description="Multi-pocket tactical & utility cargo pants."
        )

        # Brands
        brand_zenzee, _ = Brand.objects.get_or_create(
            name="ZENZEE Studio", description="In-house youth streetwear brand."
        )
        brand_urban, _ = Brand.objects.get_or_create(
            name="Urban Edge", description="Modern street culture apparel."
        )

        # Sizes
        sizes = [
            ('Small', 'S'),
            ('Medium', 'M'),
            ('Large', 'L'),
            ('Extra Large', 'XL'),
        ]
        created_sizes = []
        for name, code in sizes:
            sz, _ = Size.objects.get_or_create(name=name, code=code)
            created_sizes.append(sz)

        # Sample Products
        products_data = [
            {
                'name': 'ZENZEE Cyberpunk Heavyweight Oversized Hoodie',
                'category': cat_oversized,
                'brand': brand_zenzee,
                'description': '400 GSM 100% Cotton fleece. Drop shoulder oversized fit engineered for supreme comfort and streetwear style.',
                'price': 2999.00,
                'discount_price': 1499.00,
                'is_featured': True,
                'is_trending': True,
            },
            {
                'name': 'Tokyo Drift Graphic Oversized Acid Wash Tee',
                'category': cat_streetwear,
                'brand': brand_urban,
                'description': '240 GSM combed cotton. Vintage acid wash aesthetic with high-density puff print graphic on the back.',
                'price': 1599.00,
                'discount_price': 999.00,
                'is_featured': True,
                'is_trending': True,
            },
            {
                'name': 'Tactical Multi-Pocket Cargo Utility Pants',
                'category': cat_cargo,
                'brand': brand_zenzee,
                'description': 'Durable ripstop cotton fabric. 6 functional utility pockets with adjustable drawstring ankles.',
                'price': 2499.00,
                'discount_price': 1799.00,
                'is_featured': True,
                'is_trending': False,
            },
            {
                'name': 'Minimalist Monochrome Drop-Shoulder Sweatshirt',
                'category': cat_oversized,
                'brand': brand_zenzee,
                'description': 'Clean relaxed silhouette for daily chilling and casual wear.',
                'price': 1999.00,
                'discount_price': 1299.00,
                'is_featured': False,
                'is_trending': True,
            },
        ]

        for p_data in products_data:
            product, created = Product.objects.get_or_create(
                name=p_data['name'],
                defaults={
                    'category': p_data['category'],
                    'brand': p_data['brand'],
                    'description': p_data['description'],
                    'price': p_data['price'],
                    'discount_price': p_data['discount_price'],
                    'is_featured': p_data['is_featured'],
                    'is_trending': p_data['is_trending'],
                }
            )
            if created:
                for sz in created_sizes:
                    ProductSize.objects.get_or_create(product=product, size=sz, stock_quantity=25)

        self.stdout.write(self.style.SUCCESS("Successfully seeded ZENZEE platform data!"))
