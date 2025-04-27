# Tài liệu API Quản lý Admin

## Tổng quan

API quản lý admin cung cấp các chức năng để quản lý hệ thống từ góc nhìn của admin. Các chức năng chính bao gồm:

1. Thống kê dashboard
2. Quản lý phê duyệt bất động sản
3. Quản lý người dùng
4. Quản lý cảnh báo

API base URL: `/api/admin-api/`

## Xác thực

Tất cả các API yêu cầu xác thực bằng JWT token, sử dụng header:
```
Authorization: Bearer <token>
```

Token được lấy từ API đăng nhập:
```
POST /api/user/users/login/
```

Chỉ người dùng có quyền admin mới được phép truy cập các API này.

## I. Thống kê Dashboard

### 1. Lấy thống kê tổng quan

```
GET /api/admin-api/admin/statistics/
```

**Response:**

```json
{
    "total_users": 14,
    "total_landlords": 3,
    "total_tenants": 3,
    "total_listings": 10,
    "pending_listings": 0,
    "approved_listings": 0,
    "rejected_listings": 0,
    "new_users_this_month": 7,
    "new_listings_this_month": 1,
    "average_listing_price": 0
}
```

## II. Quản lý Phê duyệt

### 1. Danh sách bất động sản chờ phê duyệt

```
GET /api/admin-api/admin/pending_listings/
```

**Response:**

```json
{
    "count": 5,
    "next": "http://localhost:8000/api/admin-api/admin/pending_listings/?page=2",
    "previous": null,
    "results": [
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "landlord": "550e8400-e29b-41d4-a716-446655440001",
            "title": "Căn hộ cao cấp trung tâm",
            "description": "Căn hộ cao cấp với đầy đủ tiện nghi",
            "price": "8000000.00",
            "area": "50.00",
            "property_type": "apartment",
            "province": 1,
            "district": 1,
            "ward": 1,
            "street": 1,
            "specific_address": "Số 123, Nguyễn Huệ",
            "status": "pending",
            "posting_date": "2024-05-10T14:30:00Z",
            "images": [
                {"image_url": "https://example.com/image1.jpg"}
            ]
        }
    ]
}
```

### 2. Phê duyệt bất động sản

```
POST /api/admin-api/admin/approve_listing/
```

**Request:**

```json
{
    "listing_id": "550e8400-e29b-41d4-a716-446655440000",
    "action": "approve",
    "reason": "Đạt yêu cầu chất lượng"
}
```

**Response:**

```json
{
    "id": "550e8400-e29b-41d4-a716-446655440002",
    "listing": "550e8400-e29b-41d4-a716-446655440000",
    "admin": "550e8400-e29b-41d4-a716-446655440003",
    "admin_email": "admin@example.com",
    "action": "approve",
    "reason": "Đạt yêu cầu chất lượng",
    "approval_date": "2024-05-15T10:30:00Z"
}
```

### 3. Danh sách landlord chờ phê duyệt KYC

```
GET /api/admin-api/admin/pending_landlords/
```

**Response:**

```json
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": "550e8400-e29b-41d4-a716-446655440001",
            "email": "landlord@example.com",
            "first_name": "Nguyễn",
            "last_name": "Văn A",
            "phone": "0912345678",
            "user_type": "landlord",
            "kyc_status": "pending"
        }
    ]
}
```

### 4. Phê duyệt KYC cho landlord

```
POST /api/admin-api/admin/approve_landlord/
```

**Request:**

```json
{
    "user_id": "550e8400-e29b-41d4-a716-446655440001",
    "approve": true,
    "reason": "Giấy tờ hợp lệ"
}
```

**Response:**

```json
{
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "email": "landlord@example.com",
    "kyc_status": "verified",
    "message": "Đã cập nhật trạng thái KYC thành công"
}
```

## III. Quản lý Người dùng

### 1. Tìm kiếm và lọc người dùng

```
GET /api/admin-api/admin/user_management/?q=nguyen&user_type=tenant
```

**Parameters:**

- `q`: Từ khóa tìm kiếm (email, tên, số điện thoại)
- `user_type`: Lọc theo loại người dùng (tenant, landlord)

**Response:**

```json
{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": "550e8400-e29b-41d4-a716-446655440004",
            "email": "nguyen@example.com",
            "first_name": "Nguyễn",
            "last_name": "Văn B",
            "user_type": "tenant",
            "kyc_status": "pending",
            "date_joined": "2024-05-01T10:00:00Z"
        }
    ]
}
```

### 2. Vô hiệu hóa tài khoản người dùng

```
POST /api/admin-api/admin/disable_user/
```

**Request:**

```json
{
    "user_id": "550e8400-e29b-41d4-a716-446655440004",
    "reason": "Vi phạm điều khoản sử dụng"
}
```

**Response:**

```json
{
    "message": "Đã vô hiệu hóa người dùng nguyen@example.com",
    "reason": "Vi phạm điều khoản sử dụng"
}
```

## IV. Quản lý Bất động sản

### 1. Tìm kiếm và lọc bất động sản

```
GET /api/admin-api/admin/listing_management/?q=chung cư&status=approved&property_type=apartment
```

**Parameters:**

- `q`: Từ khóa tìm kiếm (tiêu đề, mô tả, địa chỉ)
- `status`: Lọc theo trạng thái (pending, approved, rejected)
- `property_type`: Lọc theo loại bất động sản (room, apartment, house)

**Response:**

```json
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "landlord": "550e8400-e29b-41d4-a716-446655440001",
            "title": "Chung cư cao cấp",
            "description": "Căn hộ chung cư cao cấp",
            "price": "10000000.00",
            "area": "60.00",
            "property_type": "apartment",
            "province": 1,
            "district": 1,
            "ward": 1,
            "street": 1,
            "specific_address": "Số 456, Lê Lợi",
            "status": "approved",
            "posting_date": "2024-05-12T14:30:00Z"
        }
    ]
}
```

## V. Quản lý Cảnh báo

### 1. Danh sách cảnh báo

```
GET /api/admin-api/alerts/
```

**Parameters:**

- `alert_type`: Lọc theo loại cảnh báo
- `listing`: Lọc theo bất động sản
- `search`: Tìm kiếm theo mô tả

**Response:**

```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": "550e8400-e29b-41d4-a716-446655440005",
            "listing": "550e8400-e29b-41d4-a716-446655440000",
            "listing_title": "Chung cư cao cấp",
            "alert_type": 1,
            "alert_type_name": "Nội dung không phù hợp",
            "description": "Phát hiện hình ảnh không phù hợp",
            "detection_time": "2024-05-14T15:30:00Z"
        }
    ]
}
```

### 2. Quản lý loại cảnh báo

```
GET /api/admin-api/alert-types/
```

**Response:**

```json
[
    {
        "id": 1,
        "name": "Nội dung không phù hợp"
    },
    {
        "id": 2,
        "name": "Lừa đảo"
    }
]
```

## Các chức năng còn thiếu

1. **Dashboard nâng cao**:
   - Biểu đồ thống kê theo thời gian (tăng trưởng người dùng, bất động sản)
   - Thống kê doanh thu từ giao dịch

2. **Quản lý giao dịch**:
   - Xem và quản lý các giao dịch trong hệ thống
   - Thống kê giao dịch theo thời gian

3. **Quản lý phí dịch vụ**:
   - Thiết lập và điều chỉnh phí dịch vụ cho các loại giao dịch

4. **Backup và khôi phục dữ liệu**:
   - Công cụ sao lưu và khôi phục dữ liệu

5. **Cấu hình hệ thống**:
   - Quản lý các tham số cấu hình hệ thống
   - Bật/tắt tính năng 