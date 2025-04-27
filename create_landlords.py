#!/usr/bin/env python
import os
import django
import sys

# Set up Django environment
print("Setting up Django environment...")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
print("Django setup complete.")

# Import necessary models
try:
    print("Importing models...")
    from user_mgmt.models import User, Landlord
    print("Models imported successfully.")
except ImportError as e:
    print(f"Error importing models: {e}")
    sys.exit(1)

# List of landlord users to create
landlord_users = [
    {
        'first_name': 'Minh',
        'last_name': 'Nguyen',
        'password': '12345678',
    },
    {
        'first_name': 'Thanh',
        'last_name': 'Tran',
        'password': '12345678',
    },
    {
        'first_name': 'Hoa',
        'last_name': 'Le',
        'password': '12345678',
    },
    {
        'first_name': 'Duc',
        'last_name': 'Pham',
        'password': '12345678',
    },
    {
        'first_name': 'Linh',
        'last_name': 'Vu',
        'password': '12345678',
    },
]

def create_landlord_users():
    print("Creating 5 landlord accounts with email similar to landlord@gmail.com")
    
    # First, delete any existing users with these emails
    print("Deleting existing users...")
    deleted_count = User.objects.filter(email='landlord@gmail.com').delete()
    print(f"Deleted {deleted_count} users with email landlord@gmail.com")
    
    total_deleted = 0
    for i in range(1, 6):
        count = User.objects.filter(email=f'landlord+{i}@gmail.com').delete()
        print(f"Deleted {count} users with email landlord+{i}@gmail.com")
        total_deleted += count[0] if isinstance(count, tuple) else count
    
    print(f"Total deleted: {total_deleted}")
    
    # Create each landlord account with a unique email
    print("\nCreating new accounts:")
    created_count = 0
    for i, landlord_data in enumerate(landlord_users):
        # For the first account, use landlord@gmail.com, for others use landlord+N@gmail.com
        email = 'landlord@gmail.com' if i == 0 else f'landlord+{i}@gmail.com'
        
        try:
            print(f"Creating account {i+1} with email {email}...")
            
            # Create new user with landlord user type
            user = User.objects.create_user(
                email=email,
                password=landlord_data['password'],
                first_name=landlord_data['first_name'],
                last_name=landlord_data['last_name'],
                user_type='landlord',
                kyc_status='verified'  # Set KYC status as verified
            )
            
            # Create Landlord record linked to the User
            landlord = Landlord.objects.create(
                user=user,
                bank_info=None,
                average_rating=None,
                number_of_reviews=0
            )
            
            print(f"Created landlord account: {email} - {landlord_data['first_name']} {landlord_data['last_name']}")
            created_count += 1
            
        except Exception as e:
            print(f"Error creating {email} for {landlord_data['first_name']} {landlord_data['last_name']}: {str(e)}")
    
    print(f"\nSuccessfully created {created_count} out of 5 accounts")
    print("\nNote: All accounts use email addresses that deliver to landlord@gmail.com")
    print("Gmail treats landlord+1@gmail.com the same as landlord@gmail.com (they're aliases)")
    
    # List all landlord accounts
    print("\nListing all landlord accounts in the database:")
    landlords = User.objects.filter(user_type='landlord')
    for user in landlords:
        print(f"- {user.email}: {user.first_name} {user.last_name}")

if __name__ == "__main__":
    print("Starting landlord account creation...")
    create_landlord_users()
    print("Completed!") 