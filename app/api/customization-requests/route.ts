import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';

function db() {
  return createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY ?? process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY!,
    { auth: { autoRefreshToken: false, persistSession: false } }
  );
}

export async function POST(req: NextRequest) {
  const body = await req.json();
  if (!body.customer_email || !body.request_details) return NextResponse.json({ error: 'Missing fields' }, { status: 400 });
  const { data, error } = await db().from('customization_requests').insert([{ ...body, status: 'pending' }]).select().single();
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  return NextResponse.json(data, { status: 201 });
}

export async function GET(req: NextRequest) {
  if (req.headers.get('x-admin-key') !== process.env.ADMIN_SECRET_KEY) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  const { searchParams } = new URL(req.url);
  const status = searchParams.get('status');
  let q = db().from('customization_requests').select('*');
  if (status) q = q.eq('status', status);
  const { data } = await q.order('created_at', { ascending: false });
  return NextResponse.json(data ?? []);
}
