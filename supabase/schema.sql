-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Products table
CREATE TABLE IF NOT EXISTS products (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  name_ar VARCHAR(255),
  description TEXT,
  description_ar TEXT,
  price DECIMAL(10,2) NOT NULL,
  type VARCHAR(50) NOT NULL CHECK (type IN ('store', 'template', 'service')),
  preview_url VARCHAR(500),
  zip_file_url VARCHAR(500),
  instructions_url VARCHAR(500),
  thumbnail_url VARCHAR(500),
  screenshots JSONB DEFAULT '[]',
  features JSONB DEFAULT '[]',
  features_ar JSONB DEFAULT '[]',
  tech_stack JSONB DEFAULT '[]',
  is_active BOOLEAN DEFAULT true,
  is_featured BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Purchases table
CREATE TABLE IF NOT EXISTS purchases (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  product_id UUID REFERENCES products(id) ON DELETE SET NULL,
  customer_email VARCHAR(255) NOT NULL,
  customer_name VARCHAR(255) NOT NULL,
  amount DECIMAL(10,2) NOT NULL,
  payment_status VARCHAR(50) DEFAULT 'completed' CHECK (payment_status IN ('pending', 'completed', 'failed', 'refunded')),
  payment_method VARCHAR(50) DEFAULT 'manual',
  download_token VARCHAR(255) UNIQUE,
  download_expires_at TIMESTAMPTZ,
  download_count INTEGER DEFAULT 0,
  max_downloads INTEGER DEFAULT 5,
  includes_customization BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Customization requests table
CREATE TABLE IF NOT EXISTS customization_requests (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  purchase_id UUID REFERENCES purchases(id) ON DELETE CASCADE,
  product_id UUID REFERENCES products(id) ON DELETE SET NULL,
  customer_email VARCHAR(255) NOT NULL,
  customer_name VARCHAR(255) NOT NULL,
  request_details TEXT NOT NULL,
  color_changes TEXT,
  new_sections TEXT,
  payment_gateway TEXT,
  domain_config TEXT,
  other_changes TEXT,
  priority VARCHAR(20) DEFAULT 'normal' CHECK (priority IN ('low', 'normal', 'high', 'urgent')),
  status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'in_progress', 'review', 'completed', 'cancelled')),
  admin_notes TEXT,
  estimated_delivery TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS Policies
ALTER TABLE products ENABLE ROW LEVEL SECURITY;
ALTER TABLE purchases ENABLE ROW LEVEL SECURITY;
ALTER TABLE customization_requests ENABLE ROW LEVEL SECURITY;

-- Allow public read of active products
CREATE POLICY "Public can view active products" ON products
  FOR SELECT USING (is_active = true);

-- Allow service role full access
CREATE POLICY "Service role full access products" ON products
  FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "Service role full access purchases" ON purchases
  FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "Service role full access customization" ON customization_requests
  FOR ALL USING (auth.role() = 'service_role');

-- Allow customers to insert purchases
CREATE POLICY "Anyone can create purchase" ON purchases
  FOR INSERT WITH CHECK (true);

-- Allow customers to insert customization requests
CREATE POLICY "Anyone can create customization request" ON customization_requests
  FOR INSERT WITH CHECK (true);

-- Updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_products_updated_at BEFORE UPDATE ON products
  FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

CREATE TRIGGER update_customization_requests_updated_at BEFORE UPDATE ON customization_requests
  FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

-- Sample products
INSERT INTO products (name, name_ar, description, description_ar, price, type, preview_url, thumbnail_url, features, features_ar, tech_stack, is_featured) VALUES
(
  'Professional E-Commerce Store',
  'متجر إلكتروني احترافي',
  'A fully-featured e-commerce store with product management, cart, checkout, and payment integration.',
  'متجر إلكتروني متكامل مع إدارة المنتجات، سلة التسوق، إتمام الشراء، وبوابات الدفع.',
  299.00,
  'store',
  'https://demo-store.vercel.app',
  'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=800',
  '["نظام إدارة منتجات متكامل", "بوابات دفع متعددة", "لوحة تحكم المدير", "تصميم متجاوب", "SEO محسّن"]',
  '["نظام إدارة منتجات متكامل", "بوابات دفع متعددة", "لوحة تحكم المدير", "تصميم متجاوب", "SEO محسّن"]',
  '["Next.js", "Supabase", "Tailwind CSS", "Stripe"]',
  true
),
(
  'Restaurant Ordering System',
  'نظام طلبات مطعم',
  'Complete restaurant management system with online ordering, table reservations, and kitchen dashboard.',
  'نظام إدارة مطعم متكامل مع طلبات أونلاين، حجز طاولات، ولوحة المطبخ.',
  249.00,
  'store',
  'https://demo-restaurant.vercel.app',
  'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800',
  '["قائمة طعام تفاعلية", "نظام حجز الطاولات", "لوحة المطبخ", "تتبع الطلبات", "دعم التوصيل"]',
  '["قائمة طعام تفاعلية", "نظام حجز الطاولات", "لوحة المطبخ", "تتبع الطلبات", "دعم التوصيل"]',
  '["React", "Node.js", "PostgreSQL", "Socket.io"]',
  true
),
(
  'Portfolio & Agency Template',
  'قالب بورتفوليو وموقع شركة',
  'Modern portfolio template for agencies and freelancers with project showcase and contact forms.',
  'قالب بورتفوليو عصري للشركات والمستقلين مع عرض المشاريع ونماذج التواصل.',
  149.00,
  'template',
  'https://demo-portfolio.vercel.app',
  'https://images.unsplash.com/photo-1467232004584-a241de8bcf5d?w=800',
  '["تصميم عصري وأنيق", "أنيميشن سلس", "نموذج تواصل", "معرض مشاريع", "متوافق مع الجوال"]',
  '["تصميم عصري وأنيق", "أنيميشن سلس", "نموذج تواصل", "معرض مشاريع", "متوافق مع الجوال"]',
  '["Next.js", "Framer Motion", "Tailwind CSS"]',
  false
);
