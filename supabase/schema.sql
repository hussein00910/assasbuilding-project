-- Run this in Supabase SQL Editor
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS products (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  name_ar VARCHAR(255),
  description TEXT,
  description_ar TEXT,
  price DECIMAL(10,2) NOT NULL DEFAULT 0,
  type VARCHAR(50) NOT NULL DEFAULT 'store',
  preview_url VARCHAR(500),
  zip_file_url VARCHAR(500),
  instructions_url VARCHAR(500),
  thumbnail_url VARCHAR(500),
  features JSONB DEFAULT '[]',
  features_ar JSONB DEFAULT '[]',
  tech_stack JSONB DEFAULT '[]',
  is_active BOOLEAN DEFAULT true,
  is_featured BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS purchases (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  product_id UUID REFERENCES products(id) ON DELETE SET NULL,
  customer_email VARCHAR(255) NOT NULL,
  customer_name VARCHAR(255) NOT NULL,
  amount DECIMAL(10,2) NOT NULL DEFAULT 0,
  payment_status VARCHAR(50) DEFAULT 'completed',
  payment_method VARCHAR(50) DEFAULT 'manual',
  download_token VARCHAR(255) UNIQUE,
  download_expires_at TIMESTAMPTZ,
  download_count INTEGER DEFAULT 0,
  max_downloads INTEGER DEFAULT 5,
  includes_customization BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS customization_requests (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  purchase_id UUID,
  product_id UUID REFERENCES products(id) ON DELETE SET NULL,
  customer_email VARCHAR(255) NOT NULL,
  customer_name VARCHAR(255),
  request_details TEXT NOT NULL,
  color_changes TEXT,
  new_sections TEXT,
  payment_gateway TEXT,
  domain_config TEXT,
  other_changes TEXT,
  status VARCHAR(50) DEFAULT 'pending',
  admin_notes TEXT,
  completed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Disable RLS for simplicity (service role key handles auth)
ALTER TABLE products DISABLE ROW LEVEL SECURITY;
ALTER TABLE purchases DISABLE ROW LEVEL SECURITY;
ALTER TABLE customization_requests DISABLE ROW LEVEL SECURITY;

-- Sample data
INSERT INTO products (name, name_ar, description_ar, price, type, preview_url, thumbnail_url, features_ar, tech_stack, is_featured, is_active) VALUES
('Professional E-Commerce Store', 'متجر إلكتروني احترافي', 'متجر إلكتروني متكامل مع إدارة المنتجات، سلة التسوق، إتمام الشراء، وبوابات الدفع.', 299.00, 'store', 'https://demo-store.vercel.app', 'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=800', '["نظام إدارة منتجات متكامل", "بوابات دفع متعددة", "لوحة تحكم المدير", "تصميم متجاوب", "SEO محسّن"]', '["Next.js", "Supabase", "Tailwind CSS", "Stripe"]', true, true),
('Restaurant Ordering System', 'نظام طلبات مطعم', 'نظام إدارة مطعم متكامل مع طلبات أونلاين، حجز طاولات، ولوحة المطبخ.', 249.00, 'store', 'https://demo-restaurant.vercel.app', 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800', '["قائمة طعام تفاعلية", "نظام حجز الطاولات", "لوحة المطبخ", "تتبع الطلبات", "دعم التوصيل"]', '["React", "Node.js", "PostgreSQL"]', true, true),
('Portfolio Agency Template', 'قالب بورتفوليو وموقع شركة', 'قالب بورتفوليو عصري للشركات والمستقلين مع عرض المشاريع ونماذج التواصل.', 149.00, 'template', 'https://demo-portfolio.vercel.app', 'https://images.unsplash.com/photo-1467232004584-a241de8bcf5d?w=800', '["تصميم عصري وأنيق", "أنيميشن سلس", "نموذج تواصل", "معرض مشاريع", "متوافق مع الجوال"]', '["Next.js", "Framer Motion", "Tailwind CSS"]', false, true)
ON CONFLICT DO NOTHING;
