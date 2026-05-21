'use client';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Plus, Pencil, Eye, EyeOff, ExternalLink } from 'lucide-react';
import { Product } from '@/lib/types';
import { formatPrice } from '@/lib/utils';

export default function AdminProducts() {
  const router = useRouter();
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);

  const adminKey = typeof window !== 'undefined' ? sessionStorage.getItem('admin_key') ?? '' : '';

  useEffect(() => {
    if (!sessionStorage.getItem('admin_key')) { router.push('/admin'); return; }
    fetch('/api/products', { headers: { 'x-admin-key': adminKey } })
      .then((r) => r.json())
      .then((d) => { setProducts(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  async function toggleActive(id: string, current: boolean) {
    await fetch(`/api/products/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json', 'x-admin-key': adminKey },
      body: JSON.stringify({ is_active: !current }),
    });
    setProducts((prev) => prev.map((p) => p.id === id ? { ...p, is_active: !current } : p));
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-white">إدارة المنتجات</h1>
        <Link href="/admin/products/new"
          className="flex items-center gap-2 bg-brand-400 text-dark-900 font-bold px-4 py-2.5 rounded-xl hover:opacity-90 text-sm">
          <Plus className="w-4 h-4" />منتج جديد
        </Link>
      </div>

      {loading ? (
        <div className="text-center text-slate-400 py-12">جاري التحميل...</div>
      ) : (
        <div className="bg-dark-700 border border-dark-500 rounded-2xl overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-dark-800 text-slate-400">
                <th className="text-right px-4 py-3 font-medium">المنتج</th>
                <th className="text-right px-4 py-3 font-medium">النوع</th>
                <th className="text-right px-4 py-3 font-medium">السعر</th>
                <th className="text-right px-4 py-3 font-medium">الحالة</th>
                <th className="text-right px-4 py-3 font-medium">إجراءات</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-dark-600">
              {products.map((p) => (
                <tr key={p.id} className="hover:bg-dark-600/50">
                  <td className="px-4 py-3 text-white font-medium">{p.name_ar || p.name}</td>
                  <td className="px-4 py-3 text-slate-400">{{ store: 'متجر', template: 'قالب', service: 'خدمة' }[p.type]}</td>
                  <td className="px-4 py-3 text-brand-400 font-bold">{formatPrice(p.price)}</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-0.5 rounded-full text-xs font-semibold ${
                      p.is_active ? 'bg-green-500/20 text-green-400' : 'bg-slate-500/20 text-slate-400'
                    }`}>{p.is_active ? 'نشط' : 'مخفي'}</span>
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-2">
                      <button onClick={() => toggleActive(p.id, p.is_active)} className="text-slate-400 hover:text-white transition-colors">
                        {p.is_active ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                      </button>
                      <Link href={`/admin/products/${p.id}/edit`} className="text-slate-400 hover:text-brand-400 transition-colors">
                        <Pencil className="w-4 h-4" />
                      </Link>
                      {p.preview_url && (
                        <a href={p.preview_url} target="_blank" rel="noopener noreferrer" className="text-slate-400 hover:text-brand-400 transition-colors">
                          <ExternalLink className="w-4 h-4" />
                        </a>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
