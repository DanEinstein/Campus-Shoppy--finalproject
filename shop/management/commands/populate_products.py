from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shop.models import Product, Category
from author.models import AuthorProfile


class Command(BaseCommand):
    help = 'Populate database with sample products for Campus Shoppy MVP'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Starting product population...'))
        
        # Create or get categories
        categories_data = [
            {'name': 'Clothing', 'photo': 'products_category/clothing'},
            {'name': 'Electronics', 'photo': 'products_category/electronics'},
            {'name': 'Books', 'photo': 'products_category/books'},
            {'name': 'Accessories', 'photo': 'products_category/accessories'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'photo': cat_data['photo']}
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created category: {category.name}'))
            else:
                self.stdout.write(f'  Category already exists: {category.name}')
        
        # Get or create author
        author = AuthorProfile.objects.first()
        if not author:
            # Create a default user and author if none exists
            user, created = User.objects.get_or_create(
                username='admin',
                defaults={
                    'email': 'admin@campusshoppy.com',
                    'is_staff': True,
                    'is_superuser': True
                }
            )
            if created:
                user.set_password('admin123')
                user.save()
                self.stdout.write(self.style.SUCCESS('✓ Created admin user'))
            
            author, created = AuthorProfile.objects.get_or_create(
                user=user,
                defaults={
                    'bio': 'Campus Shoppy Official Store',
                    'photo': 'authors/default_author'
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS('✓ Created author profile'))
        
        # Sample products with Cloudinary Public IDs
        # NOTE: These are placeholder IDs. Replace with actual Cloudinary Public IDs after uploading images
        products_data = [
            # Clothing
            {
                'name': 'Maseno University Hoodie',
                'photo': 'products/hoodie_maseno',
                'price': 2500.00,
                'details': 'Official Maseno University branded hoodie. Made from premium cotton blend for maximum comfort. Perfect for campus life and casual wear.',
                'category': 'Clothing',
                'inventory': 50,
                'featured': True
            },
            {
                'name': 'Campus T-Shirt - Blue',
                'photo': 'products/tshirt_blue',
                'price': 1200.00,
                'details': 'Comfortable 100% cotton t-shirt in university blue. Breathable fabric perfect for Kenyan weather.',
                'category': 'Clothing',
                'inventory': 100,
                'featured': True
            },
            {
                'name': 'Campus T-Shirt - White',
                'photo': 'products/tshirt_white',
                'price': 1200.00,
                'details': 'Classic white cotton t-shirt. Versatile and comfortable for everyday wear.',
                'category': 'Clothing',
                'inventory': 100,
                'featured': False
            },
            {
                'name': 'University Polo Shirt',
                'photo': 'products/polo_shirt',
                'price': 1800.00,
                'details': 'Smart casual polo shirt with university logo. Perfect for presentations and formal campus events.',
                'category': 'Clothing',
                'inventory': 60,
                'featured': True
            },
            {
                'name': 'Campus Jacket',
                'photo': 'products/jacket_campus',
                'price': 3500.00,
                'details': 'Warm and stylish campus jacket. Water-resistant material ideal for rainy season.',
                'category': 'Clothing',
                'inventory': 30,
                'featured': False
            },
            
            # Electronics
            {
                'name': 'USB Flash Drive 32GB',
                'photo': 'products/usb_32gb',
                'price': 800.00,
                'details': 'High-speed 32GB USB 3.0 flash drive. Perfect for storing assignments and projects.',
                'category': 'Electronics',
                'inventory': 150,
                'featured': True
            },
            {
                'name': 'Wireless Mouse',
                'photo': 'products/wireless_mouse',
                'price': 1500.00,
                'details': 'Ergonomic wireless mouse with long battery life. Compatible with all laptops.',
                'category': 'Electronics',
                'inventory': 80,
                'featured': False
            },
            {
                'name': 'Laptop Cooling Pad',
                'photo': 'products/cooling_pad',
                'price': 2200.00,
                'details': 'Adjustable laptop cooling pad with dual fans. Prevents overheating during long study sessions.',
                'category': 'Electronics',
                'inventory': 40,
                'featured': False
            },
            {
                'name': 'Power Bank 20000mAh',
                'photo': 'products/powerbank_20000',
                'price': 2800.00,
                'details': 'High-capacity power bank with fast charging. Never run out of battery on campus.',
                'category': 'Electronics',
                'inventory': 70,
                'featured': True
            },
            {
                'name': 'Earphones with Mic',
                'photo': 'products/earphones',
                'price': 600.00,
                'details': 'Quality earphones with built-in microphone. Perfect for online classes and music.',
                'category': 'Electronics',
                'inventory': 120,
                'featured': False
            },
            
            # Books
            {
                'name': 'Engineering Mathematics Textbook',
                'photo': 'products/book_engineering_math',
                'price': 1500.00,
                'details': 'Comprehensive engineering mathematics textbook. Essential for engineering students.',
                'category': 'Books',
                'inventory': 25,
                'featured': False
            },
            {
                'name': 'Biology Lab Manual',
                'photo': 'products/book_biology_lab',
                'price': 1200.00,
                'details': 'Complete biology laboratory manual with detailed experiments and procedures.',
                'category': 'Books',
                'inventory': 30,
                'featured': False
            },
            {
                'name': 'Research Methods Guide',
                'photo': 'products/book_research_methods',
                'price': 1800.00,
                'details': 'Essential guide for conducting academic research. Perfect for final year projects.',
                'category': 'Books',
                'inventory': 20,
                'featured': True
            },
            
            # Accessories
            {
                'name': 'Laptop Bag - Professional',
                'photo': 'products/laptop_bag_pro',
                'price': 3500.00,
                'details': 'Durable laptop bag with multiple compartments. Fits up to 15.6" laptops. Water-resistant material.',
                'category': 'Accessories',
                'inventory': 45,
                'featured': True
            },
            {
                'name': 'Backpack - Student Edition',
                'photo': 'products/backpack_student',
                'price': 2800.00,
                'details': 'Spacious student backpack with laptop compartment. Ergonomic design for comfort.',
                'category': 'Accessories',
                'inventory': 60,
                'featured': True
            },
            {
                'name': 'Water Bottle - 1L',
                'photo': 'products/water_bottle',
                'price': 500.00,
                'details': 'BPA-free water bottle with campus logo. Stay hydrated throughout the day.',
                'category': 'Accessories',
                'inventory': 200,
                'featured': False
            },
            {
                'name': 'Notebook Set (5 pack)',
                'photo': 'products/notebook_set',
                'price': 800.00,
                'details': 'Set of 5 quality notebooks. 200 pages each. Perfect for all your classes.',
                'category': 'Accessories',
                'inventory': 150,
                'featured': False
            },
            {
                'name': 'Pen Set - Premium',
                'photo': 'products/pen_set',
                'price': 400.00,
                'details': 'Set of 10 premium ballpoint pens. Smooth writing experience.',
                'category': 'Accessories',
                'inventory': 180,
                'featured': False
            },
            {
                'name': 'Campus ID Card Holder',
                'photo': 'products/id_holder',
                'price': 300.00,
                'details': 'Durable ID card holder with lanyard. Keep your student ID safe and accessible.',
                'category': 'Accessories',
                'inventory': 250,
                'featured': False
            },
            {
                'name': 'Study Lamp - LED',
                'photo': 'products/study_lamp',
                'price': 1800.00,
                'details': 'Adjustable LED study lamp with USB charging port. Energy-efficient and eye-friendly.',
                'category': 'Accessories',
                'inventory': 35,
                'featured': False
            },
        ]
        
        created_count = 0
        existing_count = 0
        
        for product_data in products_data:
            category = categories[product_data['category']]
            
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults={
                    'photo': product_data['photo'],
                    'price': product_data['price'],
                    'details': product_data['details'],
                    'category': category,
                    'author': author,
                    'inventory': product_data['inventory'],
                    'featured': product_data['featured'],
                    'is_draft': False
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created: {product.name} (KSh {product.price})'))
            else:
                existing_count += 1
                self.stdout.write(f'  Already exists: {product.name}')
        
        self.stdout.write('\n' + '='*70)
        self.stdout.write(self.style.SUCCESS(f'✓ Product population complete!'))
        self.stdout.write(self.style.SUCCESS(f'  - Created: {created_count} new products'))
        self.stdout.write(f'  - Existing: {existing_count} products')
        self.stdout.write(f'  - Total: {Product.objects.count()} products in database')
        self.stdout.write(f'  - Categories: {Category.objects.count()}')
        self.stdout.write('='*70)
        
        self.stdout.write('\n' + self.style.WARNING('IMPORTANT NOTES:'))
        self.stdout.write('1. The product images use placeholder Cloudinary Public IDs')
        self.stdout.write('2. Upload actual product images to Cloudinary and update the IDs')
        self.stdout.write('3. Image format: "products/image_name" (no file extension)')
        self.stdout.write('4. Run "python manage.py createsuperuser" if you need admin access')
