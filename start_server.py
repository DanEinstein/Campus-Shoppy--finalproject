#!/usr/bin/env python
"""
Stable Django server startup script
Handles connection issues and provides better error handling
"""

import os
import sys
import subprocess
import signal
import time
from pathlib import Path

def setup_environment():
    """Setup environment variables for stable server operation"""
    os.environ['DJANGO_SETTINGS_MODULE'] = 'django_ecommerce.settings'
    os.environ['PYTHONUNBUFFERED'] = '1'
    os.environ['DJANGO_DEBUG'] = 'True'
    
    # Add current directory to Python path
    current_dir = Path(__file__).parent
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))

def check_requirements():
    """Check if all requirements are met"""
    print("Checking requirements...")
    
    # Check if manage.py exists
    if not Path("manage.py").exists():
        print("❌ manage.py not found. Please run this script from the project root directory.")
        return False
    
    # Check if virtual environment exists
    venv_path = Path("venv")
    if not venv_path.exists():
        print("❌ Virtual environment not found.")
        print("Please create it with: python -m venv venv")
        return False
    
    # Check if Django is installed
    try:
        import django
        print(f"✅ Django {django.get_version()} found")
    except ImportError:
        print("❌ Django not found. Please install requirements: pip install -r requirements.txt")
        return False
    
    return True

def run_migrations():
    """Run database migrations"""
    print("Running database migrations...")
    try:
        subprocess.run([sys.executable, "manage.py", "migrate"], check=True)
        print("✅ Migrations completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Migration failed: {e}")
        return False

def collect_static():
    """Collect static files"""
    print("Collecting static files...")
    try:
        subprocess.run([sys.executable, "manage.py", "collectstatic", "--noinput"], check=True)
        print("✅ Static files collected")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Static collection failed: {e}")
        return False

def start_server():
    """Start the Django development server with stable configuration"""
    print("\n🚀 Starting Campus Shoppy Server...")
    print("Server will be available at: http://127.0.0.1:8000")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Start server with stable settings
        cmd = [
            sys.executable, "manage.py", "runserver",
            "127.0.0.1:8000",
            "--noreload",
            "--insecure",
            "--verbosity=1"
        ]
        
        process = subprocess.Popen(cmd)
        
        # Handle graceful shutdown
        def signal_handler(sig, frame):
            print("\n🛑 Stopping server...")
            process.terminate()
            process.wait()
            print("✅ Server stopped")
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Wait for process
        process.wait()
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        return False
    
    return True

def main():
    """Main function"""
    print("=" * 60)
    print("🏫 Campus Shoppy - Stable Server Startup")
    print("=" * 60)
    
    # Setup environment
    setup_environment()
    
    # Check requirements
    if not check_requirements():
        input("Press Enter to exit...")
        return
    
    # Run migrations
    if not run_migrations():
        input("Press Enter to exit...")
        return
    
    # Collect static files
    collect_static()
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()
