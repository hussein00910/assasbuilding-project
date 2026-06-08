'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import toast from 'react-hot-toast';

export default function NewProduct() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [f, setF] = useState({ name:'', name_ar:'', description_ar:'', price:'', type:'store', preview_url:'', zip_file_url:'', thumbnail_url:'', features_ar:'', tech_stack:'', is_featured: false });
  const u = (k: string, v: any) => setF(p => ({...p, [k]: v}));

  async function submit(e: React.FormEvent) {
    e.preventDefault(); setLoading(true);
    const ak = sessionStorage.getItem('ak') ?? '';
    const payload = { ...f, price: parseFloat(f.price), features_ar: f.features_ar.split('\n').filter(Boolean), features: f.features_ar.split('\n').filter(Boolean), tech_stack: f.tech_stack.split(',').map(s=>s.trim()).filter(Boolean), description: f.description_ar };
    try {
      const res = await fetch('/api/products', { method:'POST', headers:{'Content-Type':'application/json','x-admin-key':ak}, body: JSON.stringify(payload) });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error);
      toast.success('تم الإضافة!');
      router.push('/admin/products');
    } catch (err: any) { toast.error(err.message || 'حدث خطأ'); } finally { setLoading(false); }
  }

  const inp = "w-full bg-[#0e0e1a] border border-[#2a2a4a] text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-cyan-400";

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-white mb-6">إضافة منتج جديد</h1>
      <form onSubmit={submit} className="bg-[#16162a] border border-[#2a2a4a] rounded-2xl p-6 space-y-4">
        <div className="grid md:grid-cols-2 gap-4">
          <div><label className="block text-slate-400 text-sm mb-1">اسم عربي *</label><input required type="text" value={f.name_ar} onChange={e=>u('name_ar',e.target.value)} className={inp} /></div>
          <div><label className="block text-slate-400 text-sm mb-1">اسم إنجليزي *</label><input required type="text" value={f.name} onChange={e=>u('name',e.target.value)} className={inp} /></div>
          <div><label className="block text-slate-400 text-sm mb-1">السعر ($) *</label><input required type="number" step="0.01" value={f.price} onChange={e=>u('price',e.target.value)} className={inp} /></div>
          <div><label className="block text-slate-400 text-sm mb-1">النوع</label><select value={f.type} onChange={e=>u('type',e.target.value)} className={inp}><option value="store">متجر</option><option value="template">قالب</option><option value="service">خدمة</option></select></div>
        </div>
        <div><label className="block text-slate-400 text-sm mb-1">الوصف</label><textarea rows={3} value={f.description_ar} onChange={e=>u('description_ar',e.target.value)} className={inp+' resize-none'} /></div>
        <div><label className="block text-slate-400 text-sm mb-1">المميزات (سطر لكل ميزة)</label><textarea rows={4} value={f.features_ar} onChange={e=>u('features_ar',e.target.value)} className={inp+' resize-none'} /></div>
        <div><label className="block text-slate-400 text-sm mb-1">التقنيات (مفصولة بفاصلة)</label><input type="text" value={f.tech_stack} onChange={e=>u('tech_stack',e.target.value)} placeholder="Next.js, Supabase, Tailwind CSS" className={inp} /></div>
        <div className="grid md:grid-cols-2 gap-4">
          <div><label className="block text-slate-400 text-sm mb-1">رابط المعاينة (Vercel)</label><input type="url" value={f.preview_url} onChange={e=>u('preview_url',e.target.value)} className={inp} /></div>
          <div><label className="block text-slate-400 text-sm mb-1">رابط صورة الغلاف</label><input type="url" value={f.thumbnail_url} onChange={e=>u('thumbnail_url',e.target.value)} className={inp} /></div>
          <div><label className="block text-slate-400 text-sm mb-1">رابط ملف ZIP</label><input type="url" value={f.zip_file_url} onChange={e=>u('zip_file_url',e.target.value)} className={inp} /></div>
        </div>
        <div className="flex items-center gap-2"><input type="checkbox" id="feat" checked={f.is_featured} onChange={e=>u('is_featured',e.target.checked)} className="w-4 h-4 accent-cyan-400" /><label htmlFor="feat" className="text-slate-400 text-sm">منتج مميز</label></div>
        <button type="submit" disabled={loading} className="w-full bg-gradient-to-r from-cyan-500 to-cyan-400 text-gray-900 font-bold py-3 rounded-xl hover:opacity-90 disabled:opacity-60">{loading ? 'جاري الحفظ...' : 'إضافة المنتج'}</button>
      </form>
    </div>
  );
}
