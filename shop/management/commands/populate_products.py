from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
<<<<<<< HEAD
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
=======
from shop.models import Category, Product
from author.models import AuthorProfile
import random
# Note: We no longer need to import File, settings, or os


class Command(BaseCommand):
    help = "Syncs the database with a predefined list of products using Cloudinary Public IDs. Creates or updates products as needed."

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING(
            "--- IMPORTANT: Make sure you have updated the 'photo' values in this script with your actual Cloudinary Public IDs! ---"
        ))

        # --- NO LONGER DELETING DATA ---
        # The script will now safely create or update.

        self.stdout.write("Syncing categories...")
        categories_data = [
            {"name": "Electronics", "photo": "products_category/samsung_phone_abcd12"},
            {"name": "Fashion", "photo": "products_category/shoe_rack_efgh34"},
            {"name": "Home & Garden", "photo": "products_category/shoe_rack_ijkl56"},
            {"name": "Books", "photo": "products_category/shoe_rack_mnop78"},
            {"name": "Sports", "photo": "products_category/shoe_rack_qrst90"},
        ]

        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data["name"],
                defaults={"photo": cat_data["photo"]},
            )
            categories.append(category)
            if created:
                self.stdout.write(f"Created category: {category.name}")

        author, created = AuthorProfile.objects.get_or_create(
            user__username="admin",
            defaults={
                "user": User.objects.get_or_create(
                    username="admin",
                    defaults={
                        "email": "admin@campus-shoppy.com",
                        "first_name": "Campus",
                        "last_name": "Admin",
                    },
                )[0],
                "bio": "Campus Shoppy Administrator",
                "photo": "author/dankid_zyxw98",  # Example Public ID
            },
        )
        if created:
            self.stdout.write(f"Created author: {author.user.username}")

        self.stdout.write("Syncing products...")
        products_data = [
            # Electronics
            {"name": "Wireless Bluetooth Earbuds", "price": 3500, "category": "Electronics",
             "details": "High-quality wireless earbuds with noise cancellation and 8-hour battery life.", "inventory": 25, "photo": "products/bluetooth_buds_cB1HfNc"},
            {"name": "Phone Case & Screen Protector", "price": 2500, "category": "Electronics",
             "details": "Protective phone case with tempered glass screen protector for all phone models.", "inventory": 30, "photo": "products/phonecase_dfMFWYP"},
            {"name": "USB-C Cable Set", "price": 2000, "category": "Electronics",
             "details": "3-pack USB-C charging cables, 1m length, fast charging compatible.", "inventory": 40, "photo": "products/usb_cables_xyz789"},
            {"name": "Portable Power Bank", "price": 4500, "category": "Electronics",
             "details": "10000mAh power bank with fast charging and LED display.", "inventory": 20, "photo": "products/portable_powerbank_JCKsdz0"},
            {"name": "Bluetooth Speaker", "price": 4000, "category": "Electronics",
             "details": "Portable Bluetooth speaker with 12-hour battery and waterproof design.", "inventory": 15, "photo": "products/Bluetooth_speakers_ZOiSU95"},

            # Fashion
            {"name": "Canvas Sneakers", "price": 3500, "category": "Fashion",
             "details": "Comfortable canvas sneakers perfect for campus life and casual wear.", "inventory": 20, "photo": "products/canvas_speakers_7ufDOxA"},
            {"name": "Denim Jeans", "price": 4000, "category": "Fashion",
             "details": "Classic blue denim jeans with modern fit, perfect for any occasion.", "inventory": 25, "photo": "products/denim_8yjIZnX"},
            {"name": "Cotton T-Shirt", "price": 2500, "category": "Fashion",
             "details": "Soft cotton t-shirt available in multiple colors, comfortable and stylish.", "inventory": 35, "photo": "products/cotton_Tshirt_bcmZIgN"},
            {"name": "Hoodie", "price": 4500, "category": "Fashion",
             "details": "Warm and cozy hoodie with kangaroo pocket, perfect for chilly evenings.", "inventory": 18, "photo": "products/hoodies_mMRGnXm"},
            {"name": "Baseball Cap", "price": 2000, "category": "Fashion",
             "details": "Adjustable baseball cap with embroidered logo, sun protection included.", "inventory": 30, "photo": "products/baseball_cap_edAAJri"},

            # Home & Garden
            {"name": "Coffee Mug Set", "price": 3000, "category": "Home & Garden",
             "details": "Set of 4 ceramic coffee mugs with unique designs, perfect for your room.", "inventory": 20, "photo": "products/coffee_mugs_aaa111"},
            {"name": "Desk Organizer", "price": 3500, "category": "Home & Garden",
             "details": "Wooden desk organizer with compartments for pens, papers, and gadgets.", "inventory": 15, "photo": "products/desk_organizer_U19yFPO"},
            {"name": "LED String Lights", "price": 2500, "category": "Home & Garden",
             "details": "Warm white LED string lights, 10 meters, perfect for room decoration.", "inventory": 25, "photo": "products/led_string_lights_yHn8k3O"},
            {"name": "Plant Pot", "price": 2000, "category": "Home & Garden",
             "details": "Ceramic plant pot with drainage hole, perfect for succulents and small plants.", "inventory": 30, "photo": "products/plant_pot_cV5bfR8"},
            {"name": "Storage Baskets", "price": 4000, "category": "Home & Garden",
             "details": "Set of 3 woven storage baskets, great for organizing your room.", "inventory": 12, "photo": "products/storage_baskets_F8tlAP9"},

            # Books
            {"name": "Programming Fundamentals", "price": 3500, "category": "Books",
             "details": "Complete guide to programming fundamentals for computer science students.", "inventory": 20, "photo": "products/programming_book_NNY8BOP"},
            {"name": "Mathematics Textbook", "price": 4000, "category": "Books",
             "details": "Advanced mathematics textbook covering calculus and algebra.", "inventory": 15, "photo": "products/mathematics_book_0f1oyLD"},
            {"name": "Business Studies Guide", "price": 3000, "category": "Books",
             "details": "Comprehensive business studies guide for commerce students.", "inventory": 18, "photo": "products/business_book_vbdngd"},
            {"name": "Literature Anthology", "price": 2500, "category": "Books", "details": "Collection of African literature and poetry for literature students.",
             "inventory": 22, "photo": "products/literature_anthology_book_ZO3Z1Rz"},
            {"name": "Study Planner", "price": 2000, "category": "Books",
             "details": "Academic year planner with study schedules and goal tracking pages.", "inventory": 30, "photo": "products/study_planner_XrCJel7"},
        ]

        created_count = 0
        updated_count = 0
        for product_data in products_data:
            category = next(
                cat for cat in categories if cat.name == product_data["category"])

            # --- THIS IS THE KEY CHANGE ---
            # It will UPDATE a product if it exists, or CREATE it if it's new.
            product, created = Product.objects.update_or_create(
                # Find the product by its unique name
                name=product_data["name"],
                defaults={
                    "price": product_data["price"],
                    "category": category,
                    "author": author,
                    "details": product_data["details"],
                    "inventory": product_data["inventory"],
                    "is_draft": False,
                    "featured": random.choice([True, False]),
                    "photo": product_data["photo"]
                },
            )

            if created:
                created_count += 1
                self.stdout.write(f"Created product: {product.name}")
            else:
                updated_count += 1
                self.stdout.write(f"Updated product: {product.name}")

        self.stdout.write(self.style.SUCCESS(
            f"\nSync complete! Created {created_count} new products and updated {updated_count} existing products."
        ))
>>>>>>> e98667db69d90c224f57b1968017e6c7d554d3cd
