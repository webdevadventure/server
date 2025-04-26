#!/usr/bin/env python
import requests
import json

# URL của API đăng nhập
LOGIN_URL = "http://localhost:8000/api/user/users/login/"  # Đã sửa URL theo cấu trúc đúng

# Thông tin đăng nhập
TEST_EMAIL = '23521718@gm.uit.edu.vn'
TEST_PASSWORD = '12345678'

def test_login_api():
    """Gọi API đăng nhập và kiểm tra kết quả"""
    
    login_data = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    
    print(f"Đang thử đăng nhập với email: {TEST_EMAIL}")
    print(f"URL: {LOGIN_URL}")
    
    try:
        # Gọi API đăng nhập
        response = requests.post(LOGIN_URL, json=login_data)
        
        # In thông tin response
        print(f"\nStatus code: {response.status_code}")
        
        try:
            response_data = response.json()
            print(f"Response data: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
            
            if response.status_code == 200:
                print("\n✓ Đăng nhập thành công!")
                print(f"- Access token: {response_data.get('access')[:20]}...")
                print(f"- User ID: {response_data.get('user', {}).get('id')}")
                print(f"- User type: {response_data.get('user', {}).get('user_type')}")
            else:
                print("\n✗ Đăng nhập thất bại!")
                
        except json.JSONDecodeError:
            print(f"Response không phải định dạng JSON: {response.text}")
            
    except requests.RequestException as e:
        print(f"Lỗi khi gọi API: {str(e)}")

if __name__ == "__main__":
    print("\n=== KIỂM TRA API ĐĂNG NHẬP ===\n")
    test_login_api()
    print("\nKiểm tra hoàn tất!") 