-- Đổi tên schema auth để tránh xung đột với Supabase
CREATE SCHEMA IF NOT EXISTS user_mgmt;
CREATE SCHEMA IF NOT EXISTS location;
CREATE SCHEMA IF NOT EXISTS listing;
CREATE SCHEMA IF NOT EXISTS transaction;
CREATE SCHEMA IF NOT EXISTS blog;
CREATE SCHEMA IF NOT EXISTS admin;

-- ENUMs
DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_type_enum') THEN
        CREATE TYPE user_mgmt.user_type_enum AS ENUM ('landlord', 'tenant');
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'kyc_status_enum') THEN
        CREATE TYPE user_mgmt.kyc_status_enum AS ENUM ('pending', 'verified', 'rejected');
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'property_type_enum') THEN
        CREATE TYPE listing.property_type_enum AS ENUM ('room', 'apartment', 'house');
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'listing_status_enum') THEN
        CREATE TYPE listing.listing_status_enum AS ENUM ('pending', 'approved', 'rejected');
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'transaction_status_enum') THEN
        CREATE TYPE transaction.transaction_status_enum AS ENUM ('pending', 'completed', 'failed');
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'transaction_type_enum') THEN
        CREATE TYPE transaction.transaction_type_enum AS ENUM ('deposit', 'payment');
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'comment_target_enum') THEN
        CREATE TYPE blog.comment_target_enum AS ENUM ('listing', 'blog');
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'approval_action_enum') THEN
        CREATE TYPE admin.approval_action_enum AS ENUM ('approve', 'reject');
    END IF;
END $$;

-- user_mgmt schema (trước là auth)
CREATE TABLE user_mgmt.users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),  -- dùng UUID để đồng bộ với Supabase Auth
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    password_hash TEXT NOT NULL,
    user_type user_mgmt.user_type_enum NOT NULL,
    kyc_status user_mgmt.kyc_status_enum DEFAULT 'pending',
    deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE user_mgmt.landlords (
    landlord_id UUID PRIMARY KEY REFERENCES user_mgmt.users(user_id),
    bank_info JSONB,
    average_rating NUMERIC(2,1) CHECK (average_rating >= 0 AND average_rating <= 5),
    number_of_reviews INTEGER DEFAULT 0
);

CREATE TABLE user_mgmt.tenants (
    tenant_id UUID PRIMARY KEY REFERENCES user_mgmt.users(user_id),
    rental_history JSONB
);

-- location schema
CREATE TABLE location.provinces (
    province_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE location.cities (
    city_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    province_id INTEGER NOT NULL REFERENCES location.provinces(province_id)
);

CREATE TABLE location.districts (
    district_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    city_id INTEGER NOT NULL REFERENCES location.cities(city_id)
);

CREATE TABLE location.wards (
    ward_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    district_id INTEGER NOT NULL REFERENCES location.districts(district_id)
);

CREATE TABLE location.streets (
    street_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    ward_id INTEGER NOT NULL REFERENCES location.wards(ward_id)
);

-- listing schema
CREATE TABLE listing.listings (
    listing_id SERIAL PRIMARY KEY,
    landlord_id UUID NOT NULL REFERENCES user_mgmt.users(user_id),
    title TEXT NOT NULL,
    description TEXT,
    price NUMERIC(12,2) NOT NULL CHECK (price >= 0),
    property_type listing.property_type_enum NOT NULL,
    province_id INTEGER REFERENCES location.provinces(province_id),
    district_id INTEGER REFERENCES location.districts(district_id),
    ward_id INTEGER REFERENCES location.wards(ward_id),
    street_id INTEGER REFERENCES location.streets(street_id),
    specific_address TEXT,
    status listing.listing_status_enum DEFAULT 'pending',
    posting_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE listing.listing_images (
    image_id SERIAL PRIMARY KEY,
    listing_id INTEGER NOT NULL REFERENCES listing.listings(listing_id),
    image_url TEXT NOT NULL
);

CREATE TABLE listing.reviews (
    review_id SERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL REFERENCES user_mgmt.users(user_id),
    listing_id INTEGER NOT NULL REFERENCES listing.listings(listing_id),
    review_text TEXT,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- transaction schema
CREATE TABLE transaction.payment_methods (
    method_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE transaction.transactions (
    transaction_id SERIAL PRIMARY KEY,
    sender_id UUID NOT NULL REFERENCES user_mgmt.users(user_id),
    receiver_id UUID NOT NULL REFERENCES user_mgmt.users(user_id),
    listing_id INTEGER REFERENCES listing.listings(listing_id),
    amount NUMERIC(12,2) NOT NULL CHECK (amount >= 0),
    status transaction.transaction_status_enum DEFAULT 'pending',
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    transaction_type transaction.transaction_type_enum NOT NULL,
    method_id INTEGER REFERENCES transaction.payment_methods(method_id)
);

-- blog schema
CREATE TABLE blog.categories (
    category_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE blog.blog_posts (
    post_id SERIAL PRIMARY KEY,
    author_id UUID NOT NULL REFERENCES user_mgmt.users(user_id),
    title TEXT NOT NULL,
    content TEXT,
    posting_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    category_id INTEGER REFERENCES blog.categories(category_id)
);

CREATE TABLE blog.comments (
    comment_id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES user_mgmt.users(user_id),
    target_type blog.comment_target_enum NOT NULL,
    target_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    posting_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- admin schema
CREATE TABLE admin.admins (
    admin_id UUID PRIMARY KEY REFERENCES user_mgmt.users(user_id),
    assigned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE admin.listing_approvals (
    approval_id SERIAL PRIMARY KEY,
    listing_id INTEGER NOT NULL REFERENCES listing.listings(listing_id),
    admin_id UUID NOT NULL REFERENCES user_mgmt.users(user_id),
    action admin.approval_action_enum NOT NULL,
    reason TEXT,
    approval_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE admin.alert_types (
    alert_type_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE admin.alerts (
    alert_id SERIAL PRIMARY KEY,
    listing_id INTEGER NOT NULL REFERENCES listing.listings(listing_id),
    alert_type_id INTEGER NOT NULL REFERENCES admin.alert_types(alert_type_id),
    description TEXT,
    detection_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);