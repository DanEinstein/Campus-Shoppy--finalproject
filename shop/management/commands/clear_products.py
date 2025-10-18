from django.core.management.base import BaseCommand
from shop.models import Product, Category


class Command(BaseCommand):
    help = 'Clear all products and categories (use with caution)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm that you want to delete all products',
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(
                self.style.WARNING('This will delete ALL products and categories!')
            )
            self.stdout.write(
                self.style.WARNING('Use --confirm flag to proceed')
            )
            return

        # Delete all products first (to avoid foreign key constraints)
        product_count = Product.objects.count()
        Product.objects.all().delete()
        
        # Delete all categories
        category_count = Category.objects.count()
        Category.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS(f'Deleted {product_count} products and {category_count} categories')
        )
