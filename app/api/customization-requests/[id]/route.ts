import { NextRequest, NextResponse } from 'next/server';
import { supabaseAdmin } from '@/lib/supabaseAdmin';

export async function PATCH(req: NextRequest, { params }: { params: { id: string } }) {
  const adminKey = req.headers.get('x-admin-key');
  if (adminKey !== process.env.ADMIN_SECRET_KEY) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const body = await req.json();
  const updateData: Record<string, unknown> = { ...body };

  if (body.status === 'completed') {
    updateData.completed_at = new Date().toISOString();
  }

  const { data, error } = await supabaseAdmin
    .from('customization_requests')
    .update(updateData)
    .eq('id', params.id)
    .select()
    .single();

  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  return NextResponse.json(data);
}
