#!/usr/bin/env python
import os
import django
import json

# Thiết lập môi trường Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# Import các model và module cần thiết
from django.contrib.auth import authenticate
from user_mgmt.models import User

# Thông tin đăng nhập cần kiểm tra
TEST_EMAIL = '23521718@gm.uit.edu.vn'
TEST_PASSWORD = '12345678'

def test_user_exists():
    """Kiểm tra xem user có tồn tại không"""
    try:
        user = User.objects.get(email=TEST_EMAIL)
        print(f"✓ User tồn tại với email: {TEST_EMAIL}")
        print(f"  - ID: {user.id}")
        print(f"  - Họ tên: {user.first_name} {user.last_name}")
        print(f"  - Loại người dùng: {user.user_type}")
        print(f"  - Mật khẩu (đã hash): {user.password[:20]}...")
        
        # Kiểm tra các trường required
        if not user.user_type:
            print(f"✗ Thiếu trường user_type!")
        if not user.first_name or not user.last_name:
            print(f"✗ Thiếu trường first_name hoặc last_name!")
            
        return user
    except User.DoesNotExist:
        print(f"✗ User với email {TEST_EMAIL} không tồn tại!")
        return None

def test_authenticate():
    """Kiểm tra chức năng xác thực"""
    user = authenticate(email=TEST_EMAIL, password=TEST_PASSWORD)
    if user:
        print(f"✓ Xác thực thành công với email: {TEST_EMAIL}")
        return True
    else:
        print(f"✗ Xác thực thất bại với email: {TEST_EMAIL} và mật khẩu: {TEST_PASSWORD}")
        # In thông tin debug
        print("\nThông tin debug:")
        try:
            user = User.objects.get(email=TEST_EMAIL)
            print(f"  - User tồn tại trong database")
            print(f"  - Password sử dụng phương thức hash: {user.password[:10]}...")
            print(f"  - Authentication backends trong settings: Kiểm tra settings.py")
        except User.DoesNotExist:
            print(f"  - User không tồn tại trong database")
        return False

if __name__ == "__main__":
    print("\n=== KIỂM TRA ĐĂNG NHẬP ===\n")
    
    user = test_user_exists()
    if user:
        test_authenticate()
    
    print("\nKiểm tra hoàn tất!") 