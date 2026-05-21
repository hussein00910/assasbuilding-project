import { NextRequest, NextResponse } from 'next/server';
import { supabaseAdmin } from '@/lib/supabaseAdmin';

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const type = searchParams.get('type');
  const featured = searchParams.get('featured');

  let query = supabaseAdmin.from('products').select('*').eq('is_active', true);

  if (type) query = query.eq('type', type);
  if (featured === 'true') query = query.eq('is_featured', true);

  query = query.order('created_at', { ascending: false });

  const { data, error } = await query;
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  return NextResponse.json(data);
}

export async function POST(req: NextRequest) {
  const adminKey = req.headers.get('x-admin-key');
  if (adminKey !== process.env.ADMIN_SECRET_KEY) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const body = await req.json();
  const { data, error } = await supabaseAdmin.from('products').insert([body]).select().single();
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  return NextResponse.json(data, { status: 201 });
}
