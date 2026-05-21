import { NextRequest, NextResponse } from 'next/server';
import { supabaseAdmin } from '@/lib/supabaseAdmin';
import { sendDownloadEmail } from '@/lib/email';
import { generateToken } from '@/lib/utils';

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { product_id, customer_email, customer_name, includes_customization } = body;

    const { data: product, error: productError } = await supabaseAdmin
      .from('products')
      .select('*')
      .eq('id', product_id)
      .single();

    if (productError || !product) {
      return NextResponse.json({ error: 'Product not found' }, { status: 404 });
    }

    const downloadToken = generateToken(64);
    const expiresAt = new Date();
    expiresAt.setDate(expiresAt.getDate() + 30);

    const amount = includes_customization ? product.price + 99 : product.price;

    const { data: purchase, error } = await supabaseAdmin
      .from('purchases')
      .insert([{
        product_id,
        customer_email,
        customer_name,
        amount,
        payment_status: 'completed',
        payment_method: 'manual',
        download_token: downloadToken,
        download_expires_at: expiresAt.toISOString(),
        includes_customization: includes_customization ?? false,
      }])
      .select()
      .single();

    if (error) return NextResponse.json({ error: error.message }, { status: 500 });

    const appUrl = process.env.NEXT_PUBLIC_APP_URL ?? 'http://localhost:3000';
    const downloadUrl = `${appUrl}/api/download/${downloadToken}`;

    try {
      await sendDownloadEmail({
        to: customer_email,
        customerName: customer_name,
        productName: product.name_ar ?? product.name,
        downloadUrl,
        expiresAt: expiresAt.toISOString(),
      });
    } catch (emailErr) {
      console.error('Email send failed:', emailErr);
    }

    return NextResponse.json({
      purchase_id: purchase.id,
      download_url: downloadUrl,
      expires_at: expiresAt.toISOString(),
      includes_customization,
    }, { status: 201 });
  } catch (err) {
    console.error(err);
    return NextResponse.json({ error: 'Server error' }, { status: 500 });
  }
}

export async function GET(req: NextRequest) {
  const adminKey = req.headers.get('x-admin-key');
  if (adminKey !== process.env.ADMIN_SECRET_KEY) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const { data, error } = await supabaseAdmin
    .from('purchases')
    .select('*, product:products(name, name_ar, type)')
    .order('created_at', { ascending: false });

  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  return NextResponse.json(data);
}
