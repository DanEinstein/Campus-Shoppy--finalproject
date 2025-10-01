from setuptools import setup, find_packages

setup(
    name="campus-shoppy",
    version="1.0.0",
    description="Campus Shoppy E-commerce Platform",
    author="Campus Shoppy Team",
    packages=find_packages(),
    install_requires=[
        "Django==3.1.14",
        "Pillow",
        "django-ckeditor",
        "python-decouple",
        "whitenoise",
        "gunicorn==21.2.0",
        "paystack",
        "requests",
    ],
    python_requires=">=3.11",
)
