#!/usr/bin/env python
import os
import django

# Thiết lập môi trường Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# Import các model cần thiết
from user_mgmt.models import User
from admin_custom.models import Admin

# Danh sách admin cần tạo
admin_users = [
    {
        'first_name': 'Nguyễn Hà Minh',
        'last_name': 'Tuấn',
        'email': '23521718@gm.uit.edu.vn',
        'password': '12345678',
        'username': None,
    },
    {
        'first_name': 'Nguyễn Anh',
        'last_name': 'Tuấn',
        'email': '223521716@gm.uit.edu.vn',
        'password': '12345678',
        'username': None,
    },
    {
        'first_name': 'Nguyễn Trần Ngọc',
        'last_name': 'Ty',
        'email': '23521758@gm.uit.edu.vn',
        'password': '12345678',
        'username': None,
    },
    {
        'first_name': 'Phạm Hoàng',
        'last_name': 'Vinh',
        'email': '23521793@gm.uit.edu.vn',
        'password': '12345678',
        'username': None,
    },
    {
        'first_name': 'Nguyễn Viết',
        'last_name': 'Tùng',
        'email': '23521746@gm.uit.edu.vn',
        'password': '12345678',
        'username': None,
    },
]

def create_admin_users():
    for admin_data in admin_users:
        email = admin_data['email']
        
        # Kiểm tra xem user đã tồn tại chưa
        user_exists = User.objects.filter(email=email).exists()
        
        if not user_exists:
            try:
                # Tạo user mới với quyền admin sử dụng manager method để hash password
                user = User.objects.create_user(
                    email=email,
                    password=admin_data['password'],
                    first_name=admin_data['first_name'],
                    last_name=admin_data['last_name'],
                    user_type='admin',  # Đặt user_type là admin
                    is_staff=True,      # Cấp quyền staff
                    is_superuser=True   # Cấp quyền superuser
                )
                
                # Tạo bản ghi Admin liên kết với User
                admin = Admin.objects.create(user=user)
                
                print(f"Đã tạo tài khoản admin: {email}")
            except Exception as e:
                print(f"Lỗi khi tạo {email}: {str(e)}")
        else:
            # Cập nhật mật khẩu cho người dùng hiện có
            try:
                user = User.objects.get(email=email)
                user.set_password(admin_data['password'])
                user.user_type = 'admin'
                user.is_staff = True
                user.is_superuser = True
                user.save()
                
                # Kiểm tra và tạo bản ghi Admin nếu chưa có
                admin, created = Admin.objects.get_or_create(user=user)
                if created:
                    print(f"Đã thêm quyền admin cho tài khoản: {email}")
                else:
                    print(f"Đã cập nhật mật khẩu cho tài khoản admin: {email}")
            except Exception as e:
                print(f"Lỗi khi cập nhật {email}: {str(e)}")

if __name__ == "__main__":
    print("Bắt đầu tạo tài khoản admin...")
    create_admin_users()
    print("Hoàn thành!") 