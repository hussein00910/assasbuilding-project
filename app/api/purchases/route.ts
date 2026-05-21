import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';

function db() {
  return createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY ?? process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY!,
    { auth: { autoRefreshToken: false, persistSession: false } }
  );
}

function makeToken(n = 48) {
  const c = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  return Array.from({ length: n }, () => c[Math.floor(Math.random() * c.length)]).join('');
}

export async function POST(req: NextRequest) {
  const body = await req.json();
  const { product_id, customer_email, customer_name, includes_customization } = body;

  const { data: product } = await db().from('products').select('price,name_ar,zip_file_url').eq('id', product_id).single();
  if (!product) return NextResponse.json({ error: 'Product not found' }, { status: 404 });

  const token = makeToken();
  const expires = new Date(); expires.setDate(expires.getDate() + 30);
  const amount = (includes_customization ? Number(product.price) + 99 : Number(product.price));

  const { data: purchase, error } = await db().from('purchases').insert([{
    product_id, customer_email, customer_name, amount,
    payment_status: 'completed', download_token: token,
    download_expires_at: expires.toISOString(),
    includes_customization: Boolean(includes_customization),
  }]).select().single();

  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  const appUrl = process.env.NEXT_PUBLIC_APP_URL ?? 'http://localhost:3000';
  return NextResponse.json({ purchase_id: purchase.id, download_url: `${appUrl}/api/download/${token}` }, { status: 201 });
}

export async function GET(req: NextRequest) {
  if (req.headers.get('x-admin-key') !== process.env.ADMIN_SECRET_KEY) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  const { data } = await db().from('purchases').select('*').order('created_at', { ascending: false });
  return NextResponse.json(data ?? []);
}
