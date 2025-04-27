# API Documentation

## Authentication

### Lấy Token JWT
```
POST /api/token/
```
**Body:**
```json
{
    "email": "tuannguyen.02042005@gmail.com",
    "password": "password123"
}
```
**Response:**
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```
**Ví dụ:**
```bash
curl -X POST http://example.com/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"email": "tuannguyen.02042005@gmail.com", "password": "password123"}'
```

### Làm mới Token
```
POST /api/token/refresh/
```
**Body:**
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```
**Response:**
```json
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```
**Ví dụ:**
```bash
curl -X POST http://example.com/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}'
```

## User Management

### Đăng ký
```
POST /api/user/users/register/
```
**Body:**
```json
{
    "email": "nguyenvan@example.com",
    "password": "password123",
    "confirm_password": "password123",
    "first_name": "Văn",
    "last_name": "Nguyễn",
    "phone": "0901234567",
    "user_type": "tenant"
}
```
**Response:**
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "email": "nguyenvan@example.com",
        "first_name": "Văn",
        "last_name": "Nguyễn",
        "user_type": "tenant",
        "kyc_status": "pending"
    }
}
```
**Ví dụ:**
```bash
curl -X POST http://example.com/api/user/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "nguyenvan@example.com",
    "password": "password123",
    "confirm_password": "password123",
    "first_name": "Văn",
    "last_name": "Nguyễn",
    "phone": "0901234567",
    "user_type": "tenant"
  }'
```

### Đăng nhập
```
POST /api/user/users/login/
```
**Body:**
```json
{
    "email": "nguyenvan@example.com",
    "password": "password123"
}
```
**Response:** 
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "email": "nguyenvan@example.com",
        "first_name": "Văn",
        "last_name": "Nguyễn",
        "user_type": "tenant",
        "kyc_status": "pending"
    }
}
```
**Ví dụ:**
```bash
curl -X POST http://example.com/api/user/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "nguyenvan@example.com", "password": "password123"}'
```

### Quản lý người dùng
```
GET /api/user/users/
GET /api/user/users/{id}/
PATCH /api/user/users/{id}/
DELETE /api/user/users/{id}/
POST /api/user/users/{id}/verify_kyc/
POST /api/user/users/{id}/reject_kyc/
```

**Ví dụ:**
```bash
# Lấy danh sách người dùng
curl -X GET http://example.com/api/user/users/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Lấy thông tin người dùng cụ thể
curl -X GET http://example.com/api/user/users/550e8400-e29b-41d4-a716-446655440000/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Cập nhật thông tin người dùng
curl -X PATCH http://example.com/api/user/users/550e8400-e29b-41d4-a716-446655440000/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{"phone": "0909876543"}'

# Xác minh KYC
curl -X POST http://example.com/api/user/users/550e8400-e29b-41d4-a716-446655440000/verify_kyc/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Cập nhật thông tin cá nhân
```
PUT/PATCH /api/user/users/update_profile/
```
**Body:**
```json
{
    "first_name": "Văn",
    "last_name": "Nguyễn",
    "phone": "0901234567",
    "password": "new_password123",  
    "confirm_password": "new_password123"
}
```

**Lưu ý:** Tất cả các trường đều là tùy chọn. Trường `password` và `confirm_password` chỉ cần thiết khi muốn thay đổi mật khẩu.

**Response:**
```json
{
    "status": "success",
    "message": "Thông tin người dùng đã được cập nhật",
    "user": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "email": "nguyenvan@example.com",
        "first_name": "Văn",
        "last_name": "Nguyễn",
        "phone": "0901234567",
        "user_type": "tenant",
        "kyc_status": "pending"
    }
}
```

**Ví dụ:**
```bash
curl -X PATCH http://example.com/api/user/users/update_profile/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Văn",
    "last_name": "Nguyễn",
    "phone": "0901234567"
  }'
```

### Quản lý chủ nhà
```
GET /api/user/landlords/
GET /api/user/landlords/{id}/
GET /api/user/landlords/{id}/listings/
GET /api/user/landlords/{id}/transactions/
```

### Cập nhật thông tin chủ nhà
```
PUT/PATCH /api/user/landlords/update_profile/
```
**Body:**
```json
{
    "user": {
        "first_name": "Văn",
        "last_name": "Nguyễn",
        "phone": "0901234567",
        "password": "new_password123",  
        "confirm_password": "new_password123"
    },
    "bank_info": {
        "bank_name": "Vietcombank",
        "account_number": "1234567890",
        "account_holder": "NGUYEN VAN A"
    }
}
```

**Lưu ý:** Tất cả các trường đều là tùy chọn. Có thể cập nhật thông tin cá nhân hoặc thông tin ngân hàng hoặc cả hai.

**Response:**
```json
{
    "status": "success",
    "message": "Thông tin chủ nhà đã được cập nhật"
}
```

**Ví dụ:**
```bash
curl -X PATCH http://example.com/api/user/landlords/update_profile/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "bank_info": {
        "bank_name": "Vietcombank",
        "account_number": "1234567890",
        "account_holder": "NGUYEN VAN A"
    }
  }'
```

### Quản lý người thuê
```
GET /api/user/tenants/
GET /api/user/tenants/{id}/
GET /api/user/tenants/{id}/transactions/
GET /api/user/tenants/{id}/reviews/
```

### Cập nhật thông tin người thuê
```
PUT/PATCH /api/user/tenants/update_profile/
```
**Body:**
```json
{
    "user": {
        "first_name": "Văn",
        "last_name": "Nguyễn",
        "phone": "0901234567",
        "password": "new_password123",  
        "confirm_password": "new_password123"
    }
}
```

**Lưu ý:** Tất cả các trường đều là tùy chọn.

**Response:**
```json
{
    "status": "success",
    "message": "Thông tin người thuê đã được cập nhật"
}
```

**Ví dụ:**
```bash
curl -X PATCH http://example.com/api/user/tenants/update_profile/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "user": {
        "first_name": "Văn",
        "last_name": "Nguyễn",
        "phone": "0901234567"
    }
  }'
```

### Tìm kiếm người dùng
```
GET /api/user/users/search_users/
```
**Params:**
- `q`: Từ khóa tìm kiếm (bắt buộc)
- `page`, `page_size`: Phân trang

**Response:**
```json
{
    "landlords": [
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "user": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "nguyena@example.com",
                "first_name": "Nguyễn",
                "last_name": "Văn A",
                "user_type": "landlord"
            },
            "average_rating": 4.5,
            "number_of_reviews": 10
        }
    ],
    "tenants": [
        {
            "id": "550e8400-e29b-41d4-a716-446655440001",
            "user": {
                "id": "550e8400-e29b-41d4-a716-446655440001",
                "email": "nguyenb@example.com",
                "first_name": "Nguyễn",
                "last_name": "Văn B",
                "user_type": "tenant"
            }
        }
    ],
    "total_results": 2
}
```

**Ví dụ:**
```bash
# Tìm kiếm người dùng có tên Nguyễn
curl -X GET "http://example.com/api/user/users/search_users/?q=Nguyễn" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Tìm kiếm người dùng có email gmail
curl -X GET "http://example.com/api/user/users/search_users/?q=gmail" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Permissions:**
- Tất cả người dùng đều có thể sử dụng chức năng tìm kiếm này

## Location

### Tỉnh/Thành phố
```
GET /api/location/provinces/
GET /api/location/provinces/{id}/
POST /api/location/provinces/
PUT /api/location/provinces/{id}/
PATCH /api/location/provinces/{id}/
DELETE /api/location/provinces/{id}/
```
**Params:**
- `search`: Tìm kiếm theo tên
- `page`, `page_size`: Phân trang

### Quận/Huyện
```
GET /api/location/cities/
GET /api/location/cities/{id}/
POST /api/location/cities/
PUT /api/location/cities/{id}/
PATCH /api/location/cities/{id}/
DELETE /api/location/cities/{id}/
```
**Params:**
- `province`: Lọc theo province_id
- `search`: Tìm kiếm theo tên
- `page`, `page_size`: Phân trang

### Phường/Xã
```
GET /api/location/districts/
GET /api/location/districts/{id}/
POST /api/location/districts/
PUT /api/location/districts/{id}/
PATCH /api/location/districts/{id}/
DELETE /api/location/districts/{id}/
```
**Params:**
- `city`: Lọc theo city_id
- `search`: Tìm kiếm theo tên
- `page`, `page_size`: Phân trang

### Khu vực
```
GET /api/location/wards/
GET /api/location/wards/{id}/
POST /api/location/wards/
PUT /api/location/wards/{id}/
PATCH /api/location/wards/{id}/
DELETE /api/location/wards/{id}/
```
**Params:**
- `district`: Lọc theo district_id
- `search`: Tìm kiếm theo tên
- `page`, `page_size`: Phân trang

### Đường
```
GET /api/location/streets/
GET /api/location/streets/{id}/
POST /api/location/streets/
PUT /api/location/streets/{id}/
PATCH /api/location/streets/{id}/
DELETE /api/location/streets/{id}/
```
**Params:**
- `ward`: Lọc theo ward_id
- `search`: Tìm kiếm theo tên
- `page`, `page_size`: Phân trang

## Listing

### Bất động sản
```
GET /api/listing/listings/
GET /api/listing/listings/{id}/
POST /api/listing/listings/
PATCH /api/listing/listings/{id}/
DELETE /api/listing/listings/{id}/
POST /api/listing/listings/{id}/approve/
POST /api/listing/listings/{id}/reject/
GET /api/listing/listings/{id}/similar/
```

**Ví dụ:**
```bash
# Lấy danh sách bất động sản với bộ lọc
curl -X GET "http://example.com/api/listing/listings/?property_type=apartment&min_price=5000000&max_price=10000000&ward=123&ordering=-posting_date" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Đăng bất động sản mới
curl -X POST http://example.com/api/listing/listings/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Căn hộ 2 phòng ngủ Bình Thạnh",
    "description": "Căn hộ hiện đại, đầy đủ nội thất, gần trung tâm",
    "price": 8000000,
    "area": 65,
    "property_type": "apartment",
    "province": 1,
    "district": 5,
    "ward": 123,
    "street": 456,
    "specific_address": "Số 123, Đường ABC, Phường XYZ",
    "uploaded_images": [
      "https://example.com/images/img1.jpg",
      "https://example.com/images/img2.jpg"
    ]
  }'

# Lấy các bất động sản tương tự
curl -X GET http://example.com/api/listing/listings/42/similar/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Hình ảnh
```
GET /api/listing/images/
GET /api/listing/images/{id}/
POST /api/listing/images/
PUT /api/listing/images/{id}/
PATCH /api/listing/images/{id}/
DELETE /api/listing/images/{id}/
```
**Params:**
- `listing`: Lọc theo listing ID
- `page`, `page_size`: Phân trang

**Body (POST):**
```json
{
    "listing": number,
    "image_url": "string"
}
```

### Đánh giá
```
GET /api/listing/reviews/
GET /api/listing/reviews/{id}/
POST /api/listing/reviews/
PUT /api/listing/reviews/{id}/
PATCH /api/listing/reviews/{id}/
DELETE /api/listing/reviews/{id}/
```
**Params:**
- `listing`: Lọc theo listing ID
- `tenant`: Lọc theo tenant ID
- `min_rating`: Lọc đánh giá tối thiểu
- `ordering`: "review_date", "-review_date", "rating", "-rating"
- `page`, `page_size`: Phân trang

**Body (POST):**
```json
{
    "listing": number,
    "rating": number (1-5),
    "review_text": "string"
}
```

### Tìm kiếm phòng nâng cao
```
GET /api/listing/listings/search/
```
**Params:**
- `q`: Từ khóa tìm kiếm (bắt buộc)
- `min_price`, `max_price`: Lọc theo khoảng giá
- `min_area`, `max_area`: Lọc theo khoảng diện tích
- `property_type`: "room", "apartment", "house"
- `ordering`: "price", "-price", "area", "-area", "posting_date", "-posting_date"
- `page`, `page_size`: Phân trang

**Ví dụ:**
```bash
# Tìm phòng ở Quận Bình Thạnh
curl -X GET "http://example.com/api/listing/listings/search/?q=Bình%20Thạnh" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Tìm chung cư có 2 phòng ngủ
curl -X GET "http://example.com/api/listing/listings/search/?q=2%20phòng%20ngủ" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Tìm phòng ở Quận 1 với giá dưới 5 triệu
curl -X GET "http://example.com/api/listing/listings/search/?q=Quận%201&max_price=5000000" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Tìm căn hộ lớn hơn 50m2 ở Thủ Đức
curl -X GET "http://example.com/api/listing/listings/search/?q=Thủ%20Đức&min_area=50&property_type=apartment" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Tìm phòng mới đăng gần đường Nguyễn Văn Linh
curl -X GET "http://example.com/api/listing/listings/search/?q=Nguyễn%20Văn%20Linh&ordering=-posting_date" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Permissions:**
- Tất cả người dùng đều có thể sử dụng chức năng tìm kiếm này

## Blog

### Danh mục bài viết
```
GET /api/blog/categories/
GET /api/blog/categories/{id}/
POST /api/blog/categories/
PUT /api/blog/categories/{id}/
PATCH /api/blog/categories/{id}/
DELETE /api/blog/categories/{id}/
```
**Params:**
- `page`, `page_size`: Phân trang

**Body (POST):**
```json
{
    "name": "string",
    "description": "string"
}
```

**Permissions:**
- Tất cả người dùng đều có thể xem danh mục
- Chỉ admin mới có thể tạo, sửa, xóa danh mục

### Bài viết blog
```
GET /api/blog/posts/
GET /api/blog/posts/{id}/
POST /api/blog/posts/
PUT /api/blog/posts/{id}/
PATCH /api/blog/posts/{id}/
DELETE /api/blog/posts/{id}/
GET /api/blog/posts/{id}/comments/
```
**Params:**
- `category`: Lọc theo category ID
- `author`: Lọc theo author ID
- `search`: Tìm kiếm theo title, content
- `ordering`: "posting_date", "-posting_date", "title", "-title"
- `page`, `page_size`: Phân trang

**Body (POST):**
```json
{
    "title": "string",
    "content": "string",
    "category": number,
    "featured_image": "string"
}
```

**Permissions:**
- Tất cả người dùng đều có thể xem bài viết
- Người dùng đã đăng nhập có thể tạo bài viết mới
- Người dùng chỉ có thể chỉnh sửa hoặc xóa bài viết của chính mình
- Author field sẽ tự động được thiết lập dựa trên người dùng đã đăng nhập

**Ví dụ:**
```bash
# Lấy danh sách bài viết
curl -X GET "http://example.com/api/blog/posts/?category=1&ordering=-posting_date" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Tạo bài viết mới
curl -X POST http://example.com/api/blog/posts/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Kinh nghiệm thuê nhà ở quận Bình Thạnh",
    "content": "Bài viết chia sẻ kinh nghiệm khi thuê nhà ở quận Bình Thạnh...",
    "category": 1,
    "featured_image": "https://example.com/images/blog1.jpg"
  }'

# Lấy bình luận của bài viết
curl -X GET http://example.com/api/blog/posts/42/comments/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Bình luận
```
GET /api/blog/comments/
GET /api/blog/comments/{id}/
POST /api/blog/comments/
PUT /api/blog/comments/{id}/
PATCH /api/blog/comments/{id}/
DELETE /api/blog/comments/{id}/
```
**Params:**
- `target_type`: "blog"
- `target_id`: ID của bài viết
- `user`: Lọc theo user ID (người viết bình luận)
- `ordering`: "posting_date", "-posting_date"
- `page`, `page_size`: Phân trang

**Body (POST):**
```json
{
    "target_type": "blog",
    "target_id": number,
    "content": "string"
}
```

**Permissions:**
- Tất cả người dùng đều có thể xem bình luận
- Người dùng đã đăng nhập có thể tạo bình luận mới
- Người dùng chỉ có thể chỉnh sửa hoặc xóa bình luận của chính mình
- User field sẽ tự động được thiết lập dựa trên người dùng đã đăng nhập

**Ví dụ:**
```bash
# Thêm bình luận cho bài viết
curl -X POST http://example.com/api/blog/comments/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "target_type": "blog",
    "target_id": 42,
    "content": "Bài viết rất hữu ích, cảm ơn tác giả!"
  }'
```

## Transaction Management

### Giao dịch
```
GET /api/transaction/transactions/
GET /api/transaction/transactions/{id}/
POST /api/transaction/transactions/
PATCH /api/transaction/transactions/{id}/
DELETE /api/transaction/transactions/{id}/
```
**Params:**
- `sender`: Lọc theo sender ID
- `receiver`: Lọc theo receiver ID
- `status`: "pending", "completed", "cancelled"
- `listing`: Lọc theo listing ID
- `min_date`, `max_date`: Lọc theo khoảng thời gian
- `ordering`: "transaction_date", "-transaction_date", "amount", "-amount"
- `page`, `page_size`: Phân trang

**Body (POST):**
```json
{
    "listing": number,
    "amount": number,
    "payment_method": number,
    "transaction_type": "deposit|full_payment",
    "description": "string"
}
```

**Ví dụ:**
```bash
# Lấy danh sách giao dịch
curl -X GET "http://example.com/api/transaction/transactions/?status=pending" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Tạo giao dịch mới
curl -X POST http://example.com/api/transaction/transactions/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "listing": 42,
    "amount": 4000000,
    "payment_method": 1,
    "transaction_type": "deposit",
    "description": "Đặt cọc thuê nhà tháng 5/2025"
  }'
```

### Phương thức thanh toán
```
GET /api/transaction/payment-methods/
GET /api/transaction/payment-methods/{id}/
POST /api/transaction/payment-methods/
PUT /api/transaction/payment-methods/{id}/
PATCH /api/transaction/payment-methods/{id}/
DELETE /api/transaction/payment-methods/{id}/
```
**Params:**
- `page`, `page_size`: Phân trang

## Authentication Headers

Với các endpoint yêu cầu authentication, cần thêm header:
```
Authorization: Bearer <access_token>
```

## Status Codes

- `200 OK`: Yêu cầu thành công
- `201 Created`: Tạo mới thành công
- `400 Bad Request`: Lỗi dữ liệu không hợp lệ
- `401 Unauthorized`: Chưa xác thực
- `403 Forbidden`: Không có quyền truy cập
- `404 Not Found`: Không tìm thấy tài nguyên
- `500 Internal Server Error`: Lỗi server

## Error Responses

```json
{
    "detail": "Authentication credentials were not provided."
}
```

```json
{
    "detail": "You do not have permission to perform this action."
}
```

```json
{
    "field_name": ["Error message"]
}
```

## Pagination

Tất cả các API trả về danh sách đều hỗ trợ phân trang:

**Request:**
```
GET /api/resource/?page=2&page_size=10
```

**Response:**
```json
{
    "count": 100,
    "next": "http://example.com/api/resource/?page=3&page_size=10",
    "previous": "http://example.com/api/resource/?page=1&page_size=10",
    "results": [
        // items
    ]
}
```

- `count`: Tổng số bản ghi
- `next`: URL cho trang tiếp theo (null nếu không có)
- `previous`: URL cho trang trước (null nếu không có)
- `results`: Danh sách bản ghi

## Testing với Postman

### Cài đặt và chuẩn bị

1. **Tải và cài đặt Postman**
   - Tải Postman từ [website chính thức](https://www.postman.com/downloads/)
   - Cài đặt và tạo tài khoản (hoặc sử dụng không cần đăng nhập)

2. **Import Collection**
   - Tải file [Rental API Collection](https://example.com/rental-api-collection.json) (yêu cầu liên hệ admin)
   - Trong Postman, chọn "Import" > "Upload Files" và chọn file collection vừa tải

3. **Thiết lập Environment**
   - Tạo một Environment mới trong Postman
   - Thêm biến `base_url` với giá trị là URL của API (ví dụ: `http://localhost:8000` hoặc `https://api.example.com`)
   - Thêm biến `token` (để lưu access token)

### Luồng test cơ bản

1. **Đăng ký và Đăng nhập**
   - Sử dụng request "Register User" để tạo tài khoản mới
   - Sử dụng request "Login User" để lấy token
   - Token sẽ tự động được lưu vào biến môi trường `token`

2. **Tìm kiếm phòng**
   - Sử dụng request "Search Listings" với tham số `q` để tìm kiếm
   - Có thể thêm các tham số bộ lọc khác như `min_price`, `max_price`...

3. **Tạo Listing (cho Landlord)**
   - Đăng nhập với tài khoản landlord
   - Sử dụng request "Create Listing" để đăng thông tin phòng mới

4. **Tạo giao dịch (cho Tenant)**
   - Đăng nhập với tài khoản tenant
   - Xem chi tiết listing với "Get Listing Details"
   - Sử dụng request "Create Transaction" để tạo giao dịch

### Sử dụng Pre-request Scripts

Collection đã được cấu hình với pre-request scripts để tự động thêm token vào header:

```javascript
// Automatically add Authorization header if token exists
if (pm.environment.get('token')) {
    pm.request.headers.add({
        key: 'Authorization',
        value: 'Bearer ' + pm.environment.get('token')
    });
}
```

### Các Test Cases Mẫu

1. **Test đăng nhập**
   - **Thành công**: Nhập đúng email và password
   - **Thất bại**: Nhập sai password hoặc email không tồn tại

2. **Test tìm kiếm**
   - **Tìm theo địa điểm**: Nhập "Quận 1", "Bình Thạnh"...
   - **Tìm theo đặc điểm**: Nhập "2 phòng ngủ", "gần trung tâm"...
   - **Tìm với bộ lọc**: Kết hợp tìm kiếm và bộ lọc giá/diện tích

3. **Test tạo giao dịch**
   - **Valid Transaction**: Tạo giao dịch với đầy đủ thông tin hợp lệ
   - **Invalid Transaction**: Thử tạo giao dịch với số tiền âm hoặc thiếu thông tin

### Hướng dẫn sử dụng Test Runner

Postman cung cấp tính năng Test Runner để chạy tự động các test cases:

1. Chọn "Runner" từ toolbar của Postman
2. Chọn collection "Rental API"
3. Chọn environment đã thiết lập
4. Chọn các request cần test
5. Click "Run Rental API" để bắt đầu test

### Lưu ý khi test

- **Môi trường**: Đảm bảo bạn đang kết nối đúng với môi trường mong muốn (dev, staging, production)
- **Data test**: Một số request cần dữ liệu đặc biệt, hãy xem mô tả của từng request
- **Rate limiting**: API có thể có giới hạn số lượng request, nên tránh gửi quá nhiều request trong thời gian ngắn
- **Cleanup**: Sau khi test, nên xóa dữ liệu test không cần thiết (đặc biệt trên môi trường production)

### Xử lý lỗi phổ biến

- **401 Unauthorized**: Token hết hạn hoặc không hợp lệ, cần đăng nhập lại
- **403 Forbidden**: Không có quyền truy cập resource
- **404 Not Found**: Endpoint không tồn tại hoặc resource không tìm thấy
- **400 Bad Request**: Dữ liệu gửi đi không hợp lệ, kiểm tra lại request body

Để được hỗ trợ thêm về API hoặc cách test, vui lòng liên hệ: support@example.com

## Admin API

API quản lý dành riêng cho admins. Tất cả các API trong phần này đều yêu cầu quyền admin.

### Thống kê tổng quan

```
GET /api/admin-api/admin/statistics/
```

**Response:**
```json
{
    "total_users": 150,
    "total_landlords": 50,
    "total_tenants": 100,
    "total_listings": 80,
    "pending_listings": 10,
    "approved_listings": 65,
    "rejected_listings": 5,
    "new_users_this_month": 20,
    "new_listings_this_month": 15,
    "average_listing_price": 7500000.0
}
```

**Ví dụ:**
```bash
curl -X GET http://example.com/api/admin-api/admin/statistics/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Quản lý danh sách phê duyệt

#### Danh sách bất động sản chờ phê duyệt

```
GET /api/admin-api/admin/pending_listings/
```

**Response:**
```json
{
    "count": 10,
    "next": null,
    "previous": null,
    "results": [
        // Danh sách các listing đang chờ phê duyệt
    ]
}
```

**Ví dụ:**
```bash
curl -X GET http://example.com/api/admin-api/admin/pending_listings/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

#### Phê duyệt/Từ chối bất động sản

```
POST /api/admin-api/admin/approve_listing/
```

**Body:**
```json
{
    "listing_id": 42,
    "action": "approve",
    "reason": "Đã xác nhận thông tin bất động sản"
}
```

**Response:**
```json
{
    "id": 15,
    "listing": 42,
    "admin": "550e8400-e29b-41d4-a716-446655440000",
    "admin_email": "admin@example.com",
    "action": "approve",
    "reason": "Đã xác nhận thông tin bất động sản",
    "approval_date": "2025-04-27T10:30:45.123456Z"
}
```

**Ví dụ:**
```bash
curl -X POST http://example.com/api/admin-api/admin/approve_listing/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "listing_id": 42,
    "action": "approve",
    "reason": "Đã xác nhận thông tin bất động sản"
  }'
```

### Quản lý Landlord

#### Danh sách landlord chờ phê duyệt KYC

```
GET /api/admin-api/admin/pending_landlords/
```

**Response:**
```json
{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        // Danh sách landlord đang chờ duyệt KYC
    ]
}
```

**Ví dụ:**
```bash
curl -X GET http://example.com/api/admin-api/admin/pending_landlords/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

#### Phê duyệt/Từ chối KYC landlord

```
POST /api/admin-api/admin/approve_landlord/
```

**Body:**
```json
{
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "approve": true,
    "reason": "Đã xác nhận thông tin cá nhân"
}
```

**Response:**
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "landlord@example.com",
    "kyc_status": "verified",
    "message": "Đã cập nhật trạng thái KYC thành công"
}
```

**Ví dụ:**
```bash
curl -X POST http://example.com/api/admin-api/admin/approve_landlord/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "approve": true,
    "reason": "Đã xác nhận thông tin cá nhân"
  }'
```

### Quản lý người dùng

```
GET /api/admin-api/admin/user_management/
```

**Params:**
- `q`: Tìm kiếm theo email, tên, số điện thoại
- `user_type`: Lọc theo loại người dùng ("landlord" hoặc "tenant")
- `page`, `page_size`: Phân trang

**Response:**
```json
{
    "count": 150,
    "next": "http://example.com/api/admin-api/admin/user_management/?page=2",
    "previous": null,
    "results": [
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "email": "user@example.com",
            "first_name": "Nguyễn",
            "last_name": "Văn A",
            "user_type": "tenant",
            "kyc_status": "pending",
            "date_joined": "2025-03-15T08:15:30Z"
        },
        // Danh sách người dùng
    ]
}
```

**Ví dụ:**
```bash
curl -X GET "http://example.com/api/admin-api/admin/user_management/?q=nguyen&user_type=landlord" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

#### Vô hiệu hóa người dùng

```
POST /api/admin-api/admin/disable_user/
```

**Body:**
```json
{
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "reason": "Vi phạm điều khoản sử dụng"
}
```

**Response:**
```json
{
    "message": "Đã vô hiệu hóa người dùng user@example.com",
    "reason": "Vi phạm điều khoản sử dụng"
}
```

**Ví dụ:**
```bash
curl -X POST http://example.com/api/admin-api/admin/disable_user/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "reason": "Vi phạm điều khoản sử dụng"
  }'
```

### Quản lý bất động sản

```
GET /api/admin-api/admin/listing_management/
```

**Params:**
- `q`: Tìm kiếm theo tiêu đề, mô tả, địa chỉ
- `status`: Lọc theo trạng thái ("pending", "approved", "rejected")
- `property_type`: Lọc theo loại bất động sản ("room", "apartment", "house")
- `page`, `page_size`: Phân trang

**Response:**
```json
{
    "count": 80,
    "next": "http://example.com/api/admin-api/admin/listing_management/?page=2",
    "previous": null,
    "results": [
        // Danh sách bất động sản
    ]
}
```

**Ví dụ:**
```bash
curl -X GET "http://example.com/api/admin-api/admin/listing_management/?q=quận%201&status=approved" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Quản lý cảnh báo

```
GET /api/admin-api/alerts/
POST /api/admin-api/alerts/
PUT /api/admin-api/alerts/{id}/
DELETE /api/admin-api/alerts/{id}/
```

**Params:**
- `alert_type`: Lọc theo loại cảnh báo
- `listing`: Lọc theo listing ID
- `search`: Tìm kiếm theo mô tả
- `page`, `page_size`: Phân trang

**Body (POST):**
```json
{
    "listing": 42,
    "alert_type": 2,
    "description": "Phát hiện thông tin không chính xác về giá"
}
```

**Ví dụ:**
```bash
# Lấy danh sách cảnh báo
curl -X GET "http://example.com/api/admin-api/alerts/?alert_type=2" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Tạo cảnh báo mới
curl -X POST http://example.com/api/admin-api/alerts/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "listing": 42,
    "alert_type": 2,
    "description": "Phát hiện thông tin không chính xác về giá"
  }'
```

### Quản lý loại cảnh báo

```
GET /api/admin-api/alert-types/
POST /api/admin-api/alert-types/
PUT /api/admin-api/alert-types/{id}/
DELETE /api/admin-api/alert-types/{id}/
```

**Body (POST):**
```json
{
    "name": "Thông tin giả mạo"
}
```

**Ví dụ:**
```bash
# Lấy danh sách loại cảnh báo
curl -X GET http://example.com/api/admin-api/alert-types/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Tạo loại cảnh báo mới
curl -X POST http://example.com/api/admin-api/alert-types/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{"name": "Thông tin giả mạo"}'
```
