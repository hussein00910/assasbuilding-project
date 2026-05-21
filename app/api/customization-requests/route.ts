import { NextRequest, NextResponse } from 'next/server';
import { supabaseAdmin } from '@/lib/supabaseAdmin';

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const {
      purchase_id, product_id, customer_email, customer_name,
      request_details, color_changes, new_sections,
      payment_gateway, domain_config, other_changes,
    } = body;

    if (!purchase_id || !customer_email || !request_details) {
      return NextResponse.json({ error: 'Missing required fields' }, { status: 400 });
    }

    const { data, error } = await supabaseAdmin
      .from('customization_requests')
      .insert([{
        purchase_id, product_id, customer_email, customer_name,
        request_details, color_changes, new_sections,
        payment_gateway, domain_config, other_changes,
        status: 'pending',
      }])
      .select()
      .single();

    if (error) return NextResponse.json({ error: error.message }, { status: 500 });
    return NextResponse.json(data, { status: 201 });
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

  const { searchParams } = new URL(req.url);
  const status = searchParams.get('status');

  let query = supabaseAdmin
    .from('customization_requests')
    .select('*, product:products(name, name_ar)');

  if (status) query = query.eq('status', status);
  query = query.order('created_at', { ascending: false });

  const { data, error } = await query;
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  return NextResponse.json(data);
}
