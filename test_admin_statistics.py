#!/usr/bin/env python
import os
import django
import json
from decimal import Decimal

# Thiết lập môi trường Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# Import các model cần thiết
from django.utils import timezone
from django.db.models import Avg, Count
from user_mgmt.models import User, Landlord, Tenant
from listing.models import Listing

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def test_statistics():
    # Lấy thời gian hiện tại
    now = timezone.now()
    first_day_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Kiểm tra từng thống kê riêng lẻ
    stats = {}
    
    try:
        stats['total_users'] = User.objects.filter(deleted=False).count()
        print(f"✓ Tổng số người dùng: {stats['total_users']}")
    except Exception as e:
        print(f"✗ Lỗi khi đếm tổng số người dùng: {str(e)}")
        stats['total_users'] = None
    
    try:
        stats['total_landlords'] = Landlord.objects.count()
        print(f"✓ Tổng số chủ nhà: {stats['total_landlords']}")
    except Exception as e:
        print(f"✗ Lỗi khi đếm tổng số chủ nhà: {str(e)}")
        stats['total_landlords'] = None
    
    try:
        stats['total_tenants'] = Tenant.objects.count()
        print(f"✓ Tổng số người thuê: {stats['total_tenants']}")
    except Exception as e:
        print(f"✗ Lỗi khi đếm tổng số người thuê: {str(e)}")
        stats['total_tenants'] = None
    
    try:
        stats['total_listings'] = Listing.objects.filter(deleted=False).count()
        print(f"✓ Tổng số bất động sản: {stats['total_listings']}")
    except Exception as e:
        print(f"✗ Lỗi khi đếm tổng số bất động sản: {str(e)}")
        stats['total_listings'] = None
    
    try:
        stats['pending_listings'] = Listing.objects.filter(deleted=False, status='pending').count()
        print(f"✓ Số bất động sản đang chờ duyệt: {stats['pending_listings']}")
    except Exception as e:
        print(f"✗ Lỗi khi đếm số bất động sản đang chờ duyệt: {str(e)}")
        stats['pending_listings'] = None
    
    try:
        stats['approved_listings'] = Listing.objects.filter(deleted=False, status='approved').count()
        print(f"✓ Số bất động sản đã duyệt: {stats['approved_listings']}")
    except Exception as e:
        print(f"✗ Lỗi khi đếm số bất động sản đã duyệt: {str(e)}")
        stats['approved_listings'] = None
    
    try:
        stats['rejected_listings'] = Listing.objects.filter(deleted=False, status='rejected').count()
        print(f"✓ Số bất động sản bị từ chối: {stats['rejected_listings']}")
    except Exception as e:
        print(f"✗ Lỗi khi đếm số bất động sản bị từ chối: {str(e)}")
        stats['rejected_listings'] = None
    
    try:
        stats['new_users_this_month'] = User.objects.filter(date_joined__gte=first_day_of_month, deleted=False).count()
        print(f"✓ Số người dùng mới trong tháng: {stats['new_users_this_month']}")
    except Exception as e:
        print(f"✗ Lỗi khi đếm số người dùng mới trong tháng: {str(e)}")
        stats['new_users_this_month'] = None
    
    try:
        stats['new_listings_this_month'] = Listing.objects.filter(posting_date__gte=first_day_of_month, deleted=False).count()
        print(f"✓ Số bất động sản mới trong tháng: {stats['new_listings_this_month']}")
    except Exception as e:
        print(f"✗ Lỗi khi đếm số bất động sản mới trong tháng: {str(e)}")
        stats['new_listings_this_month'] = None
    
    try:
        avg_price = Listing.objects.filter(deleted=False, status='approved').aggregate(Avg('price'))['price__avg']
        stats['average_listing_price'] = avg_price if avg_price is not None else 0
        print(f"✓ Giá trung bình của bất động sản: {stats['average_listing_price']}")
    except Exception as e:
        print(f"✗ Lỗi khi tính giá trung bình của bất động sản: {str(e)}")
        stats['average_listing_price'] = None
    
    # In ra kết quả thống kê tổng hợp
    print("\n=== THỐNG KÊ ADMIN ===")
    print(json.dumps(stats, indent=2, default=decimal_default))
    
    return stats

if __name__ == "__main__":
    print("\n=== KIỂM TRA THỐNG KÊ ADMIN ===\n")
    test_statistics() 