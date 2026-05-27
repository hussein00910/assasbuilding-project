'use client';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Plus, Pencil, Eye, EyeOff } from 'lucide-react';

export default function AdminProducts() {
  const router = useRouter();
  const [products, setProducts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const ak = sessionStorage.getItem('ak');
    if (!ak) { router.push('/admin'); return; }
    fetch('/api/products').then(r => r.json()).then(d => { setProducts(Array.isArray(d) ? d : []); setLoading(false); });
  }, []);

  async function toggle(id: string, cur: boolean) {
    const ak = sessionStorage.getItem('ak') ?? '';
    await fetch(`/api/products/${id}`, { method: 'PATCH', headers: { 'Content-Type': 'application/json', 'x-admin-key': ak }, body: JSON.stringify({ is_active: !cur }) });
    setProducts(prev => prev.map(p => p.id === id ? { ...p, is_active: !cur } : p));
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-white">إدارة المنتجات</h1>
        <Link href="/admin/products/new" className="flex items-center gap-2 bg-cyan-400 text-gray-900 font-bold px-4 py-2.5 rounded-xl hover:opacity-90 text-sm">
          <Plus className="w-4 h-4" />منتج جديد
        </Link>
      </div>
      {loading ? <div className="text-center text-slate-400 py-12">جاري التحميل...</div> : (
        <div className="bg-[#16162a] border border-[#2a2a4a] rounded-2xl overflow-hidden">
          <table className="w-full text-sm">
            <thead><tr className="bg-[#0e0e1a] text-slate-400">
              <th className="text-right px-4 py-3">المنتج</th><th className="text-right px-4 py-3">النوع</th><th className="text-right px-4 py-3">السعر</th><th className="text-right px-4 py-3">الحالة</th><th className="text-right px-4 py-3">إجراءات</th>
            </tr></thead>
            <tbody className="divide-y divide-[#2a2a4a]">
              {products.map(p => (
                <tr key={p.id} className="hover:bg-[#1e1e36]/50">
                  <td className="px-4 py-3 text-white font-medium">{p.name_ar || p.name}</td>
                  <td className="px-4 py-3 text-slate-400">{{store:'متجر',template:'قالب',service:'خدمة'}[p.type as string]}</td>
                  <td className="px-4 py-3 text-cyan-400 font-bold">${p.price}</td>
                  <td className="px-4 py-3"><span className={`px-2 py-0.5 rounded-full text-xs font-semibold ${p.is_active ? 'bg-green-500/20 text-green-400' : 'bg-slate-500/20 text-slate-400'}`}>{p.is_active ? 'نشط' : 'مخفي'}</span></td>
                  <td className="px-4 py-3">
                    <div className="flex gap-2">
                      <button onClick={() => toggle(p.id, p.is_active)} className="text-slate-400 hover:text-white">{p.is_active ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}</button>
                      <Link href={`/admin/products/${p.id}/edit`} className="text-slate-400 hover:text-cyan-400"><Pencil className="w-4 h-4" /></Link>
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
