#!/usr/bin/env python
import requests
import json

# URL của API thống kê admin
STATISTICS_URL = "http://localhost:8000/api/admin-api/admin/statistics/"

# Thông tin đăng nhập admin
ADMIN_LOGIN_URL = "http://localhost:8000/api/user/users/login/"
ADMIN_EMAIL = "23521718@gm.uit.edu.vn"
ADMIN_PASSWORD = "12345678"

def get_admin_token():
    """Đăng nhập với tài khoản admin để lấy token"""
    login_data = {
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD
    }
    
    try:
        response = requests.post(ADMIN_LOGIN_URL, json=login_data)
        if response.status_code == 200:
            token_data = response.json()
            return token_data.get('access')
        else:
            print(f"Đăng nhập thất bại: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"Lỗi khi đăng nhập: {str(e)}")
        return None

def test_statistics_api():
    """Gọi API thống kê admin và kiểm tra kết quả"""
    # Lấy token xác thực
    token = get_admin_token()
    if not token:
        return
    
    print(f"Đã đăng nhập thành công, token: {token[:20]}...")
    
    # Gọi API thống kê với token xác thực
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(STATISTICS_URL, headers=headers)
        
        print(f"\nStatus code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("\n=== THỐNG KÊ ADMIN ===")
                print(json.dumps(data, indent=2, ensure_ascii=False))
                
                # Kiểm tra nếu có bất kỳ giá trị null nào
                has_null = False
                for key, value in data.items():
                    if value is None:
                        has_null = True
                        print(f"✗ Trường {key} có giá trị null")
                
                if not has_null:
                    print("\n✓ Tất cả các trường đều có giá trị không null")
            except json.JSONDecodeError:
                print(f"Lỗi: Response không phải JSON: {response.text}")
        else:
            print(f"Lỗi: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Lỗi khi gọi API: {str(e)}")

if __name__ == "__main__":
    print("\n=== KIỂM TRA API THỐNG KÊ ADMIN ===\n")
    test_statistics_api() 