#!/usr/bin/env python
import os
import django
import sys
import random
from decimal import Decimal

# Set up Django environment
print("Setting up Django environment...")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
print("Django setup complete.")

# Import necessary models
try:
    print("Importing models...")
    from user_mgmt.models import User, Landlord
    from listing.models import Listing, ListingImage, PropertyType, ListingStatus
    from location.models import Province, District, Ward, Street
    print("Models imported successfully.")
except ImportError as e:
    print(f"Error importing models: {e}")
    sys.exit(1)

# List of landlord users to create with pending KYC
landlord_users_pending = [
    {
        'first_name': 'Thanh',
        'last_name': 'Phan',
        'password': '12345678',
        'email': 'landlord_pending1@gmail.com',
    },
    {
        'first_name': 'Huong',
        'last_name': 'Tran',
        'password': '12345678',
        'email': 'landlord_pending2@gmail.com',
    },
    {
        'first_name': 'Tuan',
        'last_name': 'Dang',
        'password': '12345678',
        'email': 'landlord_pending3@gmail.com',
    },
]

# List of sample property titles
property_titles = [
    "Phòng trọ sạch sẽ gần Đại học Bách Khoa",
    "Căn hộ 2 phòng ngủ quận 7, đầy đủ nội thất",
    "Phòng trọ sinh viên có gác, gần chợ",
    "Nhà nguyên căn cho thuê, giá tốt",
    "Phòng trọ cao cấp, có ban công, gần công viên",
    "Căn hộ cao cấp view sông, nội thất sang trọng",
    "Phòng trọ cho thuê khu vực an ninh tốt",
    "Nhà nguyên căn mới xây, 3 phòng ngủ",
    "Căn hộ studio thiết kế hiện đại",
    "Phòng trọ máy lạnh, có nhà vệ sinh riêng",
    "Căn hộ 1PN, full nội thất, gần trung tâm",
    "Nhà nguyên căn hẻm ô tô, khu dân cư yên tĩnh",
]

# List of sample property descriptions
property_descriptions = [
    "Phòng trọ có gác lửng, toilet riêng, có máy lạnh, cửa sổ thoáng mát. Khu vực an ninh, gần nhiều tiện ích.",
    "Căn hộ đầy đủ nội thất cao cấp. Bao gồm tủ lạnh, máy giặt, TV, giường, tủ quần áo. Phù hợp cho gia đình nhỏ hoặc người đi làm.",
    "Nhà nguyên căn mới xây, thiết kế hiện đại, đầy đủ tiện nghi. Khu vực an ninh, cách trung tâm 10 phút đi xe.",
    "Phòng trọ rộng rãi, sạch sẽ. Có chỗ để xe, wifi miễn phí, giờ giấc tự do. Phù hợp cho sinh viên hoặc người đi làm.",
    "Căn hộ view đẹp, nội thất sang trọng. Có hồ bơi, phòng gym, khu vui chơi trẻ em trong khu chung cư.",
    "Nhà nguyên căn hai tầng, đường xe hơi vào tận cửa. Khu dân cư an ninh, yên tĩnh, gần trường học và siêu thị.",
    "Phòng trọ có ban công rộng, toilet riêng, có máy nước nóng. Giờ giấc tự do, an ninh tốt.",
    "Căn hộ mới xây 100%, nội thất cao cấp, view thành phố. Bao phí quản lý và internet tốc độ cao.",
]

# List of sample image URLs
sample_image_urls = [
    "https://cdn.houseviet.vn/images/project/23042023/the-sang-residence-ha-noi.jpg",
    "https://cdn.houseviet.vn/images/project/16052023/chung-cu-udic-westlake-ha-noi.jpg",
    "https://cdn.houseviet.vn/images/project/25042023/phu-tai-residence-binh-dinh.jpg",
    "https://cdn.houseviet.vn/images/project/05052023/tecco-felice-homes-binh-duong.jpg",
    "https://cdn.houseviet.vn/images/project/04052023/him-lam-thuan-an-binh-duong.jpg",
    "https://cdn.houseviet.vn/images/project/04052023/opal-skyline-binh-duong.jpg",
    "https://cdn.houseviet.vn/images/project/11042023/van-phuc-1-binh-duong.jpg",
    "https://cdn.houseviet.vn/images/project/20042023/new-galaxy-binh-duong.jpg",
    "https://cdn.houseviet.vn/images/project/ha-do-riverside-ha-noi.jpg",
]

def create_pending_landlords():
    """Create landlord accounts with pending KYC status"""
    print("\n=== Creating landlord accounts with pending KYC status ===")
    
    # First, delete any existing users with these emails
    print("Deleting existing users...")
    for user_data in landlord_users_pending:
        email = user_data['email']
        deleted_count = User.objects.filter(email=email).delete()
        print(f"Deleted {deleted_count} users with email {email}")
    
    # Create each landlord account 
    created_count = 0
    for landlord_data in landlord_users_pending:
        try:
            print(f"Creating account with email {landlord_data['email']}...")
            
            # Create new user with landlord user type and pending KYC status
            user = User.objects.create_user(
                email=landlord_data['email'],
                password=landlord_data['password'],
                first_name=landlord_data['first_name'],
                last_name=landlord_data['last_name'],
                user_type='landlord',
                kyc_status='pending'  # Set KYC status as pending
            )
            
            # Create Landlord record linked to the User
            landlord = Landlord.objects.create(
                user=user,
                bank_info=None,
                average_rating=None,
                number_of_reviews=0
            )
            
            print(f"Created landlord account: {landlord_data['email']} - {landlord_data['first_name']} {landlord_data['last_name']}")
            created_count += 1
            
        except Exception as e:
            print(f"Error creating {landlord_data['email']}: {str(e)}")
    
    print(f"\nSuccessfully created {created_count} landlord accounts with pending KYC status")
    
    # List all landlord accounts with pending KYC
    print("\nListing all landlord accounts with pending KYC in the database:")
    landlords = User.objects.filter(user_type='landlord', kyc_status='pending')
    for user in landlords:
        print(f"- {user.email}: {user.first_name} {user.last_name}")

def get_random_location():
    """Get random location from database or create if needed"""
    try:
        # Get or create basic location data
        province, _ = Province.objects.get_or_create(name="Thành phố Hồ Chí Minh")
        district, _ = District.objects.get_or_create(name="Quận 1", defaults={'city_id': 1})
        ward, _ = Ward.objects.get_or_create(name="Phường Bến Nghé", defaults={'district': district})
        street, _ = Street.objects.get_or_create(name="Đường Nguyễn Huệ", defaults={'ward': ward})
        
        return {
            'province': province,
            'district': district,
            'ward': ward,
            'street': street
        }
    except Exception as e:
        print(f"Error getting location data: {str(e)}")
        return None

def create_pending_listings():
    """Create listings with pending approval status"""
    print("\n=== Creating listings with pending approval status ===")
    
    # Get all verified landlords
    landlords = User.objects.filter(user_type='landlord', kyc_status='verified')
    
    if not landlords.exists():
        print("No verified landlords found! Please create landlords with verified KYC status first.")
        return
    
    # Get location data
    location = get_random_location()
    if not location:
        print("Failed to get location data. Cannot create listings.")
        return
    
    # Delete any existing pending listings
    print("Deleting existing pending listings...")
    deleted = Listing.objects.filter(status='pending').delete()
    print(f"Deleted {deleted} pending listings")
    
    # Create random listings for each landlord
    created_count = 0
    for landlord in landlords:
        # Create 1-3 listings per landlord
        num_listings = random.randint(1, 3)
        
        for i in range(num_listings):
            try:
                # Select random property details
                title = random.choice(property_titles)
                description = random.choice(property_descriptions)
                price = Decimal(str(random.randint(200, 2000) * 10000))  # 2-20 million VND
                area = Decimal(str(random.randint(15, 100)))  # 15-100 square meters
                property_type = random.choice([t[0] for t in PropertyType.choices])
                
                # Create the listing
                listing = Listing.objects.create(
                    landlord=landlord,
                    title=f"{title} #{random.randint(1000, 9999)}",  # Add random number to make titles unique
                    description=description,
                    price=price,
                    area=area,
                    property_type=property_type,
                    province=location['province'],
                    district=location['district'],
                    ward=location['ward'],
                    street=location['street'],
                    specific_address=f"Số {random.randint(1, 999)}, {location['street'].name}",
                    status=ListingStatus.PENDING
                )
                
                # Add 1-3 random images
                num_images = random.randint(1, 3)
                for j in range(num_images):
                    ListingImage.objects.create(
                        listing=listing,
                        image_url=random.choice(sample_image_urls)
                    )
                
                print(f"Created listing: '{listing.title}' for landlord {landlord.email}")
                created_count += 1
                
            except Exception as e:
                print(f"Error creating listing for {landlord.email}: {str(e)}")
    
    print(f"\nSuccessfully created {created_count} listings with pending approval status")
    
    # List all pending listings
    print("\nListing all pending listings in the database:")
    listings = Listing.objects.filter(status=ListingStatus.PENDING)
    for listing in listings:
        print(f"- '{listing.title}' by {listing.landlord.email}, Price: {listing.price} VND, Area: {listing.area} m²")

if __name__ == "__main__":
    print("Starting test data creation...")
    
    # Create landlords with pending KYC
    create_pending_landlords()
    
    # Create listings with pending approval
    create_pending_listings()
    
    print("\nCompleted!") 