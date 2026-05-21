import { NextRequest, NextResponse } from 'next/server';
import { supabaseAdmin } from '@/lib/supabaseAdmin';

export async function GET(_req: NextRequest, { params }: { params: { token: string } }) {
  const { data: purchase, error } = await supabaseAdmin
    .from('purchases')
    .select('*, product:products(name, zip_file_url)')
    .eq('download_token', params.token)
    .single();

  if (error || !purchase) {
    return NextResponse.json({ error: 'Invalid or expired download link' }, { status: 404 });
  }

  if (purchase.payment_status !== 'completed') {
    return NextResponse.json({ error: 'Payment not completed' }, { status: 403 });
  }

  if (new Date(purchase.download_expires_at) < new Date()) {
    return NextResponse.json({ error: 'Download link has expired' }, { status: 410 });
  }

  if (purchase.download_count >= purchase.max_downloads) {
    return NextResponse.json({ error: 'Download limit reached' }, { status: 429 });
  }

  await supabaseAdmin
    .from('purchases')
    .update({ download_count: purchase.download_count + 1 })
    .eq('id', purchase.id);

  const zipUrl = purchase.product?.zip_file_url;
  if (!zipUrl) {
    return NextResponse.json({ error: 'File not available' }, { status: 404 });
  }

  return NextResponse.redirect(zipUrl);
}
