import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';

function db() {
  return createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY ?? process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY!,
    { auth: { autoRefreshToken: false, persistSession: false } }
  );
}

export async function GET(_req: NextRequest, { params }: { params: { token: string } }) {
  const { data: p } = await db().from('purchases')
    .select('*, product:products(zip_file_url)')
    .eq('download_token', params.token).single();

  if (!p) return NextResponse.json({ error: 'Invalid link' }, { status: 404 });
  if (p.payment_status !== 'completed') return NextResponse.json({ error: 'Not paid' }, { status: 403 });
  if (new Date(p.download_expires_at) < new Date()) return NextResponse.json({ error: 'Link expired' }, { status: 410 });

  await db().from('purchases').update({ download_count: (p.download_count ?? 0) + 1 }).eq('id', p.id);
  const url = p.product?.zip_file_url;
  if (!url) return NextResponse.json({ error: 'File not found' }, { status: 404 });
  return NextResponse.redirect(url);
}
