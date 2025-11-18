"""
Script to clean up old/unwanted repositories
Run this once to remove the HcnQlw8oqwdMO8FowcM5WfnEwj22 / project repository
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codehubdebug.settings')
django.setup()

from core.models import Repository
from django.contrib.auth.models import User

def clean_old_repositories():
    """Remove old Firebase UID-based repositories"""
    print("🔍 Scanning for old repositories...")
    
    # Find repositories with Firebase UID as owner username
    old_repos = Repository.objects.filter(
        owner__username__startswith='Hcn'  # Firebase UIDs often start with random chars
    ) | Repository.objects.filter(
        owner__username__regex=r'^[A-Za-z0-9]{20,}$'  # Long random strings
    )
    
    if old_repos.exists():
        print(f"\n📋 Found {old_repos.count()} old repository/repositories:")
        for repo in old_repos:
            print(f"   - {repo.owner.username} / {repo.name}")
            print(f"     Created: {repo.created_at}")
            print(f"     Files: {repo.files.count()}")
        
        print("\n" + "="*50)
        confirm = input("❓ Delete these repositories? (yes/no): ").lower()
        
        if confirm == 'yes':
            count = old_repos.count()
            old_repos.delete()
            print(f"✅ Deleted {count} repository/repositories successfully!")
        else:
            print("❌ Cancelled. No repositories deleted.")
    else:
        print("✅ No old repositories found. Your database is clean!")
    
    print("\n" + "="*50)
    print("📊 Current repositories in database:")
    all_repos = Repository.objects.all()
    if all_repos.exists():
        for repo in all_repos:
            owner_name = repo.owner.first_name or repo.owner.username
            print(f"   - {owner_name} / {repo.name} ({repo.visibility})")
    else:
        print("   No repositories found.")

if __name__ == "__main__":
    try:
        clean_old_repositories()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nIf you prefer, you can delete it manually:")
        print("1. Go to Django admin: http://localhost:8000/admin/")
        print("2. Login with superuser account")
        print("3. Go to Core > Repositories")
        print("4. Find and delete the unwanted repository")
