#!/usr/bin/env python
"""
Script to create initial database migrations
"""
import os
import django
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nal_backend.settings')
    django.setup()
    
    # Create migrations for all apps
    apps = [
        'authentication',
        'users', 
        'properties',
        'documents',
        'payments',
        'bookings',
        'notifications'
    ]
    
    for app in apps:
        print(f"Creating migrations for {app}...")
        execute_from_command_line(['manage.py', 'makemigrations', app])
    
    print("Running migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("Database setup complete!")