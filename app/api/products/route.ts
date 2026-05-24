import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';

function db() {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL!;
  // Support all key formats: new publishable, legacy anon, Vercel connector
  const key =
    process.env.SUPABASE_SERVICE_ROLE_KEY ??
    process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY ??
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;
  return createClient(url, key, { auth: { autoRefreshToken: false, persistSession: false } });
}

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const type = searchParams.get('type');
  let q = db().from('products').select('*').eq('is_active', true);
  if (type) q = q.eq('type', type);
  const { data, error } = await q.order('created_at', { ascending: false });
  if (error) return NextResponse.json([], { status: 200 });
  return NextResponse.json(data ?? []);
}

export async function POST(req: NextRequest) {
  const key = req.headers.get('x-admin-key');
  if (key !== process.env.ADMIN_SECRET_KEY) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  const body = await req.json();
  const { data, error } = await db().from('products').insert([body]).select().single();
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  return NextResponse.json(data, { status: 201 });
}
