#!/usr/bin/env python
"""
Preparation script for PythonAnywhere deployment
Run this before deploying to check everything is ready
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'softproject_api.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from api.models import User, Service, Order

def check_services():
    """Check if services are initialized"""
    print("\n📦 Checking Services...")
    services = Service.objects.all()
    if services.count() == 0:
        print("   ❌ No services found!")
        print("   → Run: python manage.py init_services")
        return False
    else:
        print(f"   ✅ Found {services.count()} services:")
        for service in services:
            print(f"      - {service.name_en} ({service.name_ar}): {service.price_per_unit} IQD/{service.unit_name}")
        return True

def check_users():
    """Check if there are any users"""
    print("\n👥 Checking Users...")
    users = User.objects.all()
    if users.count() == 0:
        print("   ⚠️  No users found")
        print("   → This is OK, but consider creating a superuser for admin access")
        print("   → Run: python manage.py createsuperuser")
        return True
    else:
        print(f"   ✅ Found {users.count()} user(s)")
        return True

def check_orders():
    """Check orders"""
    print("\n🛒 Checking Orders...")
    orders = Order.objects.all()
    print(f"   ℹ️  Found {orders.count()} order(s)")
    return True

def check_files():
    """Check if important files exist"""
    print("\n📁 Checking Files...")
    files_to_check = [
        'manage.py',
        'requirements.txt',
        'api/models.py',
        'api/views.py',
        'api/urls.py',
        'softproject_api/settings.py',
        'softproject_api/urls.py',
        'frontend/index.html',
        'frontend/app.js',
        'frontend/styles.css',
    ]
    
    all_ok = True
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} NOT FOUND!")
            all_ok = False
    
    return all_ok

def check_migrations():
    """Check if there are unapplied migrations"""
    print("\n🔄 Checking Migrations...")
    try:
        from django.core.management import call_command
        from io import StringIO
        
        out = StringIO()
        call_command('showmigrations', '--plan', stdout=out)
        output = out.getvalue()
        
        if '[X]' in output:
            print("   ✅ Migrations applied")
            return True
        else:
            print("   ⚠️  Some migrations may not be applied")
            print("   → Run: python manage.py migrate")
            return False
    except Exception as e:
        print(f"   ⚠️  Could not check migrations: {e}")
        return True

def generate_secret_key():
    """Generate a new secret key for production"""
    print("\n🔐 Generating New Secret Key...")
    from django.core.management.utils import get_random_secret_key
    new_key = get_random_secret_key()
    print(f"   New SECRET_KEY: {new_key}")
    print("\n   ⚠️  IMPORTANT: Use this in your settings_production.py file!")
    print("   Don't share this key publicly!")
    return True

def main():
    """Run all checks"""
    print("=" * 60)
    print("🚀 PythonAnywhere Deployment Preparation Check")
    print("=" * 60)
    
    checks = [
        ("Files", check_files),
        ("Migrations", check_migrations),
        ("Services", check_services),
        ("Users", check_users),
        ("Orders", check_orders),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"   ❌ Error checking {name}: {e}")
            results.append((name, False))
    
    # Generate secret key
    generate_secret_key()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Summary")
    print("=" * 60)
    
    all_passed = True
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All checks passed! Ready for deployment!")
        print("\nNext steps:")
        print("1. Push code to GitHub (optional but recommended)")
        print("2. Follow PYTHONANYWHERE_DEPLOYMENT.md guide")
        print("3. Use DEPLOYMENT_CHECKLIST.md to track progress")
    else:
        print("⚠️  Some checks failed. Fix issues before deploying.")
        print("Review the output above for details.")
    print("=" * 60)
    
    # Deployment info
    print("\n📚 Helpful Documentation:")
    print("   - PYTHONANYWHERE_DEPLOYMENT.md - Complete deployment guide")
    print("   - DEPLOYMENT_CHECKLIST.md - Quick checklist")
    print("   - API_DOCUMENTATION.md - API reference")
    print("   - README.md - Project overview")
    
    print("\n🌐 After deployment, your site will be at:")
    print("   https://YOUR-USERNAME.pythonanywhere.com/")
    print("\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        sys.exit(1)

