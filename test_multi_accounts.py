#!/usr/bin/env python
import requests
import json

# URL của API đăng nhập
LOGIN_URL = "http://localhost:8000/api/user/users/login/"

# Danh sách tài khoản admin cần kiểm tra
admin_accounts = [
    {
        'email': '23521718@gm.uit.edu.vn',
        'password': '12345678',
        'name': 'Nguyễn Hà Minh Tuấn'
    },
    {
        'email': '223521716@gm.uit.edu.vn',
        'password': '12345678',
        'name': 'Nguyễn Anh Tuấn'
    },
    {
        'email': '23521758@gm.uit.edu.vn',
        'password': '12345678',
        'name': 'Nguyễn Trần Ngọc Ty'
    },
    {
        'email': '23521793@gm.uit.edu.vn',
        'password': '12345678',
        'name': 'Phạm Hoàng Vinh'
    },
    {
        'email': '23521746@gm.uit.edu.vn',
        'password': '12345678',
        'name': 'Nguyễn Viết Tùng'
    }
]

def test_login_api(account):
    """Gọi API đăng nhập và kiểm tra kết quả"""
    
    login_data = {
        "email": account['email'],
        "password": account['password']
    }
    
    print(f"\n----- Đang kiểm tra tài khoản: {account['name']} -----")
    print(f"Email: {account['email']}")
    
    try:
        # Gọi API đăng nhập
        response = requests.post(LOGIN_URL, json=login_data)
        
        # In thông tin response
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                response_data = response.json()
                print(f"✓ Đăng nhập thành công!")
                print(f"- User ID: {response_data.get('user', {}).get('id')}")
                print(f"- User type: {response_data.get('user', {}).get('user_type')}")
                return True
            except json.JSONDecodeError:
                print(f"✗ Response không phải định dạng JSON")
                print(f"Response: {response.text}")
                return False
        else:
            try:
                response_data = response.json()
                print(f"✗ Đăng nhập thất bại! Lỗi: {json.dumps(response_data, ensure_ascii=False)}")
            except json.JSONDecodeError:
                print(f"✗ Đăng nhập thất bại! Response: {response.text}")
            return False
            
    except requests.RequestException as e:
        print(f"✗ Lỗi khi gọi API: {str(e)}")
        return False

def fix_account_in_django_shell(account):
    """In ra lệnh để sửa tài khoản trong Django shell"""
    print(f"\n----- Lệnh khắc phục cho tài khoản: {account['name']} -----")
    print(f"Chạy các lệnh sau trong Django shell (python manage.py shell):")
    print(f"""
from user_mgmt.models import User
from admin_custom.models import Admin

# Tìm hoặc tạo user
try:
    user = User.objects.get(email='{account['email']}')
    print(f"Đã tìm thấy user: {{user.email}}")
except User.DoesNotExist:
    user = User.objects.create_user(
        email='{account['email']}',
        password='{account['password']}',
        first_name='{account['name'].split()[0]}',  # Điều chỉnh nếu cần
        last_name='{' '.join(account['name'].split()[1:])}',  # Điều chỉnh nếu cần
        user_type='admin',
        is_staff=True,
        is_superuser=True
    )
    print(f"Đã tạo user mới: {{user.email}}")

# Đặt lại mật khẩu
user.set_password('{account['password']}')
user.user_type = 'admin'
user.is_staff = True
user.is_superuser = True
user.save()
print(f"Đã cập nhật thông tin user")

# Tạo hoặc cập nhật bản ghi Admin
admin, created = Admin.objects.get_or_create(user=user)
if created:
    print(f"Đã tạo bản ghi Admin mới")
else:
    print(f"Đã cập nhật bản ghi Admin")
    """)

if __name__ == "__main__":
    print("\n=== KIỂM TRA ĐĂNG NHẬP CỦA CÁC TÀI KHOẢN ADMIN ===\n")
    
    success_count = 0
    failed_accounts = []
    
    for account in admin_accounts:
        if test_login_api(account):
            success_count += 1
        else:
            failed_accounts.append(account)
    
    print(f"\n=== KẾT QUẢ TỔNG QUAN ===")
    print(f"- Tổng số tài khoản: {len(admin_accounts)}")
    print(f"- Đăng nhập thành công: {success_count}")
    print(f"- Đăng nhập thất bại: {len(failed_accounts)}")
    
    if failed_accounts:
        print("\n=== HƯỚNG DẪN KHẮC PHỤC ===")
        print("Có thể cần phải sửa các tài khoản sau:")
        
        for account in failed_accounts:
            fix_account_in_django_shell(account)
    
    print("\nKiểm tra hoàn tất!") 