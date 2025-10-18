from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shop.models import Category, Product
from author.models import AuthorProfile
import random
from django.core.files import File
from django.conf import settings
import os


class Command(BaseCommand):
    help = "Populate the database with sample products for MVP"

    def handle(self, *args, **options):
        # Create categories if they don't exist
        categories_data = [
            {"name": "Electronics", "photo": "products_category/samsung_phone.jpg"},
            {"name": "Fashion", "photo": "products_category/shoe_rack.webp"},
            {"name": "Home & Garden", "photo": "products_category/shoe_rack.webp"},
            {"name": "Books", "photo": "products_category/shoe_rack.webp"},
            {"name": "Sports", "photo": "products_category/shoe_rack.webp"},
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

        # Create or get an author
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
                "photo": "author/dankid.jpg",
            },
        )
        if created:
            self.stdout.write(f"Created author: {author.user.username}")

        # Sample products data with realistic Kenyan prices (KSh 2,000-5,000)
        products_data = [
            # Electronics
            {"name": "Wireless Bluetooth Earbuds", "price": 3500, "category": "Electronics", "details": "High-quality wireless earbuds with noise cancellation and 8-hour battery life.", "inventory": 25, "photo": "products/bluetooth buds.jpg"},
            {"name": "Phone Case & Screen Protector", "price": 2500, "category": "Electronics", "details": "Protective phone case with tempered glass screen protector for all phone models.", "inventory": 30, "photo": "products/phonecase.jpg"},
            {"name": "USB-C Cable Set", "price": 2000, "category": "Electronics", "details": "3-pack USB-C charging cables, 1m length, fast charging compatible.", "inventory": 40, "photo": "products/usb cables.jpg"},
            {"name": "Portable Power Bank", "price": 4500, "category": "Electronics", "details": "10000mAh power bank with fast charging and LED display.", "inventory": 20, "photo": "products/portable powerbank.jpg"},
            {"name": "Bluetooth Speaker", "price": 4000, "category": "Electronics", "details": "Portable Bluetooth speaker with 12-hour battery and waterproof design.", "inventory": 15, "photo": "products/Bluetooth speakers.jpg"},
            
            # Fashion
            {"name": "Canvas Sneakers", "price": 3500, "category": "Fashion", "details": "Comfortable canvas sneakers perfect for campus life and casual wear.", "inventory": 20, "photo": "products/canvas speakers.jpg"},
            {"name": "Denim Jeans", "price": 4000, "category": "Fashion", "details": "Classic blue denim jeans with modern fit, perfect for any occasion.", "inventory": 25, "photo": "products/denim.jpg"},
            {"name": "Cotton T-Shirt", "price": 2500, "category": "Fashion", "details": "Soft cotton t-shirt available in multiple colors, comfortable and stylish.", "inventory": 35, "photo": "products/cotton Tshirt.jpg"},
            {"name": "Hoodie", "price": 4500, "category": "Fashion", "details": "Warm and cozy hoodie with kangaroo pocket, perfect for chilly evenings.", "inventory": 18, "photo": "products/hoodies.jpg"},
            {"name": "Baseball Cap", "price": 2000, "category": "Fashion", "details": "Adjustable baseball cap with embroidered logo, sun protection included.", "inventory": 30, "photo": "products/baseball cap.jpg"},
            
            # Home & Garden
            {"name": "Coffee Mug Set", "price": 3000, "category": "Home & Garden", "details": "Set of 4 ceramic coffee mugs with unique designs, perfect for your room.", "inventory": 20, "photo": "products/coffee mug set.jpg"},
            {"name": "Desk Organizer", "price": 3500, "category": "Home & Garden", "details": "Wooden desk organizer with compartments for pens, papers, and gadgets.", "inventory": 15, "photo": "products/desk organizer.jpg"},
            {"name": "LED String Lights", "price": 2500, "category": "Home & Garden", "details": "Warm white LED string lights, 10 meters, perfect for room decoration.", "inventory": 25, "photo": "products/led string lights.jpg"},
            {"name": "Plant Pot", "price": 2000, "category": "Home & Garden", "details": "Ceramic plant pot with drainage hole, perfect for succulents and small plants.", "inventory": 30, "photo": "products/plant pot.jpg"},
            {"name": "Storage Baskets", "price": 4000, "category": "Home & Garden", "details": "Set of 3 woven storage baskets, great for organizing your room.", "inventory": 12, "photo": "products/storage baskets.jpg"},
            
            # Books
            {"name": "Programming Fundamentals", "price": 3500, "category": "Books", "details": "Complete guide to programming fundamentals for computer science students.", "inventory": 20, "photo": "products/programming book.jpg"},
            {"name": "Mathematics Textbook", "price": 4000, "category": "Books", "details": "Advanced mathematics textbook covering calculus and algebra.", "inventory": 15, "photo": "products/mathematics book.jpg"},
            {"name": "Business Studies Guide", "price": 3000, "category": "Books", "details": "Comprehensive business studies guide for commerce students.", "inventory": 18, "photo": "products/business book.jpg"},
            {"name": "Literature Anthology", "price": 2500, "category": "Books", "details": "Collection of African literature and poetry for literature students.", "inventory": 22, "photo": "products/literature anthology book.jpg"},
            {"name": "Study Planner", "price": 2000, "category": "Books", "details": "Academic year planner with study schedules and goal tracking pages.", "inventory": 30, "photo": "products/study planner.jpg"},
        ]

        # Create or update products
        created_count = 0
        updated_count = 0
        for product_data in products_data:
            category = next(cat for cat in categories if cat.name == product_data["category"])

            product, created = Product.objects.update_or_create(
                name=product_data["name"],
                defaults={
                    "price": product_data["price"],
                    "category": category,
                    "author": author,
                    "details": product_data["details"],
                    "inventory": product_data["inventory"],
                    "is_draft": False,
                    "featured": random.choice([True, False]),
                },
            )

            # Handle the image separately
            image_path = os.path.join(settings.MEDIA_ROOT, product_data["photo"])
            if os.path.exists(image_path):
                with open(image_path, "rb") as f:
                    product.photo.save(os.path.basename(product_data["photo"]), File(f), save=True)

            if created:
                created_count += 1
                self.stdout.write(f"Created product: {product.name} - KSh {product.price}")
            else:
                updated_count += 1
                self.stdout.write(f"Updated product: {product.name} - KSh {product.price}")

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {created_count} and updated {updated_count} products!"
            )
        )
        self.stdout.write(
            self.style.SUCCESS("Your MVP store now has products to display!")
        )