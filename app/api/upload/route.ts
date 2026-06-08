import { NextRequest, NextResponse } from 'next/server';
import { supabaseAdmin } from '@/lib/supabaseAdmin';

export async function POST(req: NextRequest) {
  const adminKey = req.headers.get('x-admin-key');
  if (adminKey !== process.env.ADMIN_SECRET_KEY) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  try {
    const formData = await req.formData();
    const file = formData.get('file') as File;
    const bucket = formData.get('bucket') as string ?? 'products';
    const path = formData.get('path') as string;

    if (!file) return NextResponse.json({ error: 'No file provided' }, { status: 400 });

    const bytes = await file.arrayBuffer();
    const buffer = Buffer.from(bytes);

    const { data, error } = await supabaseAdmin.storage
      .from(bucket)
      .upload(path, buffer, {
        contentType: file.type,
        upsert: true,
      });

    if (error) return NextResponse.json({ error: error.message }, { status: 500 });

    const { data: urlData } = supabaseAdmin.storage.from(bucket).getPublicUrl(data.path);

    return NextResponse.json({ url: urlData.publicUrl });
  } catch (err) {
    console.error(err);
    return NextResponse.json({ error: 'Upload failed' }, { status: 500 });
  }
}
