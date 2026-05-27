'use client';
import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import toast from 'react-hot-toast';

export default function EditProduct() {
  const { id } = useParams();
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [f, setF] = useState<any>({});
  const u = (k: string, v: any) => setF((p: any) => ({...p, [k]: v}));

  useEffect(() => {
    fetch(`/api/products/${id}`).then(r => r.json()).then(d => {
      setF({ ...d, features_ar_text: (d.features_ar ?? []).join('\n'), tech_stack_text: (d.tech_stack ?? []).join(', ') });
      setLoading(false);
    });
  }, [id]);

  async function submit(e: React.FormEvent) {
    e.preventDefault(); setSaving(true);
    const ak = sessionStorage.getItem('ak') ?? '';
    const payload = { ...f, features_ar: (f.features_ar_text ?? '').split('\n').filter(Boolean), features: (f.features_ar_text ?? '').split('\n').filter(Boolean), tech_stack: (f.tech_stack_text ?? '').split(',').map((s: string) => s.trim()).filter(Boolean) };
    delete payload.features_ar_text; delete payload.tech_stack_text;
    try {
      const res = await fetch(`/api/products/${id}`, { method:'PATCH', headers:{'Content-Type':'application/json','x-admin-key':ak}, body: JSON.stringify(payload) });
      if (!res.ok) throw new Error();
      toast.success('تم الحفظ!'); router.push('/admin/products');
    } catch { toast.error('حدث خطأ'); } finally { setSaving(false); }
  }

  if (loading) return <div className="flex justify-center py-20"><div className="w-10 h-10 border-4 border-cyan-400 border-t-transparent rounded-full animate-spin" /></div>;
  const inp = "w-full bg-[#0e0e1a] border border-[#2a2a4a] text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-cyan-400";

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-white mb-6">تعديل المنتج</h1>
      <form onSubmit={submit} className="bg-[#16162a] border border-[#2a2a4a] rounded-2xl p-6 space-y-4">
        <div className="grid md:grid-cols-2 gap-4">
          <div><label className="block text-slate-400 text-sm mb-1">اسم عربي</label><input type="text" value={f.name_ar??''} onChange={e=>u('name_ar',e.target.value)} className={inp} /></div>
          <div><label className="block text-slate-400 text-sm mb-1">السعر ($)</label><input type="number" step="0.01" value={f.price??''} onChange={e=>u('price',parseFloat(e.target.value))} className={inp} /></div>
          <div><label className="block text-slate-400 text-sm mb-1">رابط المعاينة</label><input type="url" value={f.preview_url??''} onChange={e=>u('preview_url',e.target.value)} className={inp} /></div>
          <div><label className="block text-slate-400 text-sm mb-1">رابط ZIP</label><input type="url" value={f.zip_file_url??''} onChange={e=>u('zip_file_url',e.target.value)} className={inp} /></div>
          <div><label className="block text-slate-400 text-sm mb-1">رابط الغلاف</label><input type="url" value={f.thumbnail_url??''} onChange={e=>u('thumbnail_url',e.target.value)} className={inp} /></div>
        </div>
        <div><label className="block text-slate-400 text-sm mb-1">الوصف</label><textarea rows={3} value={f.description_ar??''} onChange={e=>u('description_ar',e.target.value)} className={inp+' resize-none'} /></div>
        <div><label className="block text-slate-400 text-sm mb-1">المميزات</label><textarea rows={4} value={f.features_ar_text??''} onChange={e=>u('features_ar_text',e.target.value)} className={inp+' resize-none'} /></div>
        <div><label className="block text-slate-400 text-sm mb-1">التقنيات</label><input type="text" value={f.tech_stack_text??''} onChange={e=>u('tech_stack_text',e.target.value)} className={inp} /></div>
        <button type="submit" disabled={saving} className="w-full bg-gradient-to-r from-cyan-500 to-cyan-400 text-gray-900 font-bold py-3 rounded-xl hover:opacity-90 disabled:opacity-60">{saving ? 'جاري الحفظ...' : 'حفظ التعديلات'}</button>
      </form>
    </div>
  );
}
