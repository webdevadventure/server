-- Cơ sở dữ liệu của hệ thống quản lý bất động sản

-- User Management Tables
CREATE TABLE user_mgmt_user (
    id UUID PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP WITH TIME ZONE NULL,
    is_superuser BOOLEAN NOT NULL,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    is_staff BOOLEAN NOT NULL,
    is_active BOOLEAN NOT NULL,
    date_joined TIMESTAMP WITH TIME ZONE NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    phone VARCHAR(20) NULL,
    user_type VARCHAR(10) NOT NULL,
    kyc_status VARCHAR(10) NOT NULL,
    deleted BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE user_mgmt_landlord (
    user_id UUID PRIMARY KEY REFERENCES user_mgmt_user(id),
    bank_info JSONB NULL,
    average_rating DECIMAL(2,1) NULL,
    number_of_reviews INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE user_mgmt_tenant (
    user_id UUID PRIMARY KEY REFERENCES user_mgmt_user(id),
    rental_history JSONB NULL
);

-- Location Tables
CREATE TABLE location_province (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE location_city (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    province_id BIGINT NOT NULL REFERENCES location_province(id)
);

CREATE TABLE location_district (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    city_id BIGINT NOT NULL REFERENCES location_city(id)
);

CREATE TABLE location_ward (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    district_id BIGINT NOT NULL REFERENCES location_district(id)
);

CREATE TABLE location_street (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    ward_id BIGINT NOT NULL REFERENCES location_ward(id)
);

-- Listing Tables
CREATE TABLE listing_listing (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NULL,
    price DECIMAL(12,2) NOT NULL,
    area DECIMAL(10,2) NULL,
    property_type VARCHAR(10) NOT NULL,
    specific_address TEXT NULL,
    status VARCHAR(10) NOT NULL,
    posting_date TIMESTAMP WITH TIME ZONE NOT NULL,
    deleted BOOLEAN NOT NULL DEFAULT FALSE,
    landlord_id UUID NOT NULL REFERENCES user_mgmt_user(id),
    province_id BIGINT NULL REFERENCES location_province(id),
    district_id BIGINT NULL REFERENCES location_district(id),
    ward_id BIGINT NULL REFERENCES location_ward(id),
    street_id BIGINT NULL REFERENCES location_street(id)
);

CREATE TABLE listing_listingimage (
    id BIGSERIAL PRIMARY KEY,
    image_url VARCHAR(200) NOT NULL,
    listing_id BIGINT NOT NULL REFERENCES listing_listing(id)
);

CREATE TABLE listing_review (
    id BIGSERIAL PRIMARY KEY,
    review_text TEXT NULL,
    rating INTEGER NOT NULL,
    review_date TIMESTAMP WITH TIME ZONE NOT NULL,
    listing_id BIGINT NOT NULL REFERENCES listing_listing(id),
    tenant_id UUID NOT NULL REFERENCES user_mgmt_user(id),
    UNIQUE(tenant_id, listing_id)
);

-- Transaction Tables
CREATE TABLE transaction_mgmt_paymentmethod (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE transaction_mgmt_transaction (
    id BIGSERIAL PRIMARY KEY,
    amount DECIMAL(12,2) NOT NULL,
    status VARCHAR(20) NOT NULL,
    transaction_date TIMESTAMP WITH TIME ZONE NOT NULL,
    transaction_type VARCHAR(20) NOT NULL,
    sender_id UUID NOT NULL REFERENCES user_mgmt_user(id),
    receiver_id UUID NOT NULL REFERENCES user_mgmt_user(id),
    listing_id BIGINT NULL REFERENCES listing_listing(id),
    payment_method_id BIGINT NULL REFERENCES transaction_mgmt_paymentmethod(id)
);

-- Blog Tables
CREATE TABLE blog_category (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE blog_blogpost (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NULL,
    posting_date TIMESTAMP WITH TIME ZONE NOT NULL,
    author_id UUID NOT NULL REFERENCES user_mgmt_user(id),
    category_id BIGINT NULL REFERENCES blog_category(id)
);

CREATE TABLE blog_comment (
    id BIGSERIAL PRIMARY KEY,
    target_type VARCHAR(10) NOT NULL,
    target_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    posting_date TIMESTAMP WITH TIME ZONE NOT NULL,
    user_id UUID NOT NULL REFERENCES user_mgmt_user(id)
);

-- Admin Tables
CREATE TABLE admin_custom_admin (
    user_id UUID PRIMARY KEY REFERENCES user_mgmt_user(id),
    assigned_date TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE TABLE admin_custom_alerttype (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE admin_custom_alert (
    id BIGSERIAL PRIMARY KEY,
    description TEXT NULL,
    detection_time TIMESTAMP WITH TIME ZONE NOT NULL,
    listing_id BIGINT NOT NULL REFERENCES listing_listing(id),
    alert_type_id BIGINT NOT NULL REFERENCES admin_custom_alerttype(id)
);

CREATE TABLE admin_custom_listingapproval (
    id BIGSERIAL PRIMARY KEY,
    action VARCHAR(10) NOT NULL,
    reason TEXT NULL,
    approval_date TIMESTAMP WITH TIME ZONE NOT NULL,
    admin_id UUID NOT NULL REFERENCES user_mgmt_user(id),
    listing_id BIGINT NOT NULL REFERENCES listing_listing(id)
);

-- Indexes
CREATE INDEX user_mgmt_user_email_idx ON user_mgmt_user(email);
CREATE INDEX user_mgmt_user_user_type_idx ON user_mgmt_user(user_type);

CREATE INDEX location_province_name_idx ON location_province(name);
CREATE INDEX location_city_province_id_idx ON location_city(province_id);
CREATE INDEX location_district_city_id_idx ON location_district(city_id);
CREATE INDEX location_ward_district_id_idx ON location_ward(district_id);
CREATE INDEX location_street_ward_id_idx ON location_street(ward_id);

CREATE INDEX listing_listing_landlord_id_idx ON listing_listing(landlord_id);
CREATE INDEX listing_listing_status_posting_date_idx ON listing_listing(status, posting_date);
CREATE INDEX listing_listing_property_type_idx ON listing_listing(property_type);
CREATE INDEX listing_listing_province_id_idx ON listing_listing(province_id);
CREATE INDEX listing_listing_district_id_idx ON listing_listing(district_id);
CREATE INDEX listing_listing_ward_id_idx ON listing_listing(ward_id);
CREATE INDEX listing_listing_price_idx ON listing_listing(price);
CREATE INDEX listing_listing_area_idx ON listing_listing(area);

CREATE INDEX listing_listingimage_listing_id_idx ON listing_listingimage(listing_id);
CREATE INDEX listing_review_listing_id_idx ON listing_review(listing_id);
CREATE INDEX listing_review_tenant_id_idx ON listing_review(tenant_id);
CREATE INDEX listing_review_rating_idx ON listing_review(rating);

CREATE INDEX transaction_mgmt_transaction_sender_id_idx ON transaction_mgmt_transaction(sender_id);
CREATE INDEX transaction_mgmt_transaction_receiver_id_idx ON transaction_mgmt_transaction(receiver_id);
CREATE INDEX transaction_mgmt_transaction_listing_id_idx ON transaction_mgmt_transaction(listing_id);
CREATE INDEX transaction_mgmt_transaction_status_idx ON transaction_mgmt_transaction(status);
CREATE INDEX transaction_mgmt_transaction_transaction_date_idx ON transaction_mgmt_transaction(transaction_date);

CREATE INDEX blog_blogpost_author_id_idx ON blog_blogpost(author_id);
CREATE INDEX blog_blogpost_category_id_idx ON blog_blogpost(category_id);
CREATE INDEX blog_comment_user_id_idx ON blog_comment(user_id);
CREATE INDEX blog_comment_target_type_target_id_idx ON blog_comment(target_type, target_id); 