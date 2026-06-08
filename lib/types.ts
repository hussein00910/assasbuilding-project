export type ProductType = 'store' | 'template' | 'service';
export type PaymentStatus = 'pending' | 'completed' | 'failed' | 'refunded';
export type RequestStatus = 'pending' | 'in_progress' | 'review' | 'completed' | 'cancelled';
export type Priority = 'low' | 'normal' | 'high' | 'urgent';

export interface Product {
  id: string;
  name: string;
  name_ar: string;
  description: string;
  description_ar: string;
  price: number;
  type: ProductType;
  preview_url: string | null;
  zip_file_url: string | null;
  instructions_url: string | null;
  thumbnail_url: string | null;
  screenshots: string[];
  features: string[];
  features_ar: string[];
  tech_stack: string[];
  is_active: boolean;
  is_featured: boolean;
  created_at: string;
  updated_at: string;
}

export interface Purchase {
  id: string;
  product_id: string;
  customer_email: string;
  customer_name: string;
  amount: number;
  payment_status: PaymentStatus;
  payment_method: string;
  download_token: string | null;
  download_expires_at: string | null;
  download_count: number;
  max_downloads: number;
  includes_customization: boolean;
  created_at: string;
  product?: Product;
}

export interface CustomizationRequest {
  id: string;
  purchase_id: string;
  product_id: string;
  customer_email: string;
  customer_name: string;
  request_details: string;
  color_changes: string | null;
  new_sections: string | null;
  payment_gateway: string | null;
  domain_config: string | null;
  other_changes: string | null;
  priority: Priority;
  status: RequestStatus;
  admin_notes: string | null;
  estimated_delivery: string | null;
  completed_at: string | null;
  created_at: string;
  updated_at: string;
  product?: Product;
}
