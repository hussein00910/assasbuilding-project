import { NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';

export async function GET() {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const key =
    process.env.SUPABASE_SERVICE_ROLE_KEY ??
    process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY ??
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
  const adminKey = process.env.ADMIN_SECRET_KEY;

  const envStatus = {
    NEXT_PUBLIC_SUPABASE_URL: url ? `✅ ${url.substring(0, 30)}...` : '❌ MISSING',
    SUPABASE_SERVICE_ROLE_KEY: process.env.SUPABASE_SERVICE_ROLE_KEY ? '✅ SET' : '❌ MISSING',
    NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY: process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY ? '✅ SET' : '❌ MISSING',
    NEXT_PUBLIC_SUPABASE_ANON_KEY: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY ? '✅ SET' : '❌ MISSING',
    ADMIN_SECRET_KEY: adminKey ? '✅ SET' : '❌ MISSING',
    active_key: key ? `✅ ${key.substring(0, 20)}...` : '❌ NO KEY FOUND',
  };

  if (!url || !key) {
    return NextResponse.json({ status: 'ERROR', message: 'Missing Supabase credentials', env: envStatus }, { status: 500 });
  }

  try {
    const db = createClient(url, key, { auth: { autoRefreshToken: false, persistSession: false } });
    const { data, error } = await db.from('products').select('count').single();
    if (error) {
      return NextResponse.json({ status: 'DB_ERROR', message: error.message, hint: error.hint, env: envStatus }, { status: 500 });
    }
    return NextResponse.json({ status: 'OK ✅', message: 'Supabase connected successfully', data, env: envStatus });
  } catch (e: any) {
    return NextResponse.json({ status: 'EXCEPTION', message: e.message, env: envStatus }, { status: 500 });
  }
}
