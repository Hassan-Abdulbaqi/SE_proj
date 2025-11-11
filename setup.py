"""
Setup script for initializing the Django project
Run: python setup.py
"""
import os
import sys
import subprocess

def run_command(command):
    """Run a shell command"""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print(result.stdout)
    return True

def main():
    print("Setting up Django project...")
    
    # Install dependencies
    print("\n1. Installing dependencies...")
    if not run_command("pip install -r requirements.txt"):
        print("Failed to install dependencies")
        return
    
    # Make migrations
    print("\n2. Creating migrations...")
    if not run_command("python manage.py makemigrations"):
        print("Failed to create migrations")
        return
    
    # Run migrations
    print("\n3. Running migrations...")
    if not run_command("python manage.py migrate"):
        print("Failed to run migrations")
        return
    
    # Initialize services
    print("\n4. Initializing services...")
    if not run_command("python manage.py init_services"):
        print("Failed to initialize services")
        return
    
    print("\n✅ Setup complete!")
    print("\nTo start the server, run:")
    print("python manage.py runserver")
    print("\nThe API will be available at: http://localhost:8000/api/")

if __name__ == "__main__":
    main()

