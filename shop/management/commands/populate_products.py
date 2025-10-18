from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
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
