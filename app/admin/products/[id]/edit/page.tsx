'use client';
import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Product } from '@/lib/types';
import toast from 'react-hot-toast';

export default function EditProduct() {
  const { id } = useParams<{ id: string }>();
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [form, setForm] = useState<Partial<Product> & { features_ar_text?: string; tech_stack_text?: string }>({});

  const adminKey = typeof window !== 'undefined' ? sessionStorage.getItem('admin_key') ?? '' : '';

  useEffect(() => {
    fetch(`/api/products/${id}`)
      .then((r) => r.json())
      .then((d: Product) => {
        setForm({
          ...d,
          features_ar_text: (d.features_ar ?? []).join('\n'),
          tech_stack_text: (d.tech_stack ?? []).join(', '),
        });
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [id]);

  function update(field: string, value: unknown) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSaving(true);
    const payload = {
      ...form,
      features_ar: (form.features_ar_text ?? '').split('\n').filter(Boolean),
      features: (form.features_ar_text ?? '').split('\n').filter(Boolean),
      tech_stack: (form.tech_stack_text ?? '').split(',').map((s: string) => s.trim()).filter(Boolean),
    };
    delete payload.features_ar_text;
    delete payload.tech_stack_text;

    try {
      const res = await fetch(`/api/products/${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json', 'x-admin-key': adminKey },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error();
      toast.success('تم الحفظ!');
      router.push('/admin/products');
    } catch {
      toast.error('حدث خطأ');
    } finally {
      setSaving(false);
    }
  }

  if (loading) return <div className="flex items-center justify-center min-h-screen"><div className="w-10 h-10 border-4 border-brand-400 border-t-transparent rounded-full animate-spin" /></div>;

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-white mb-6">تعديل المنتج</h1>
      <form onSubmit={handleSubmit} className="bg-dark-700 border border-dark-500 rounded-2xl p-6 space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-slate-400 text-sm mb-1">اسم عربي</label>
            <input type="text" value={form.name_ar ?? ''} onChange={(e) => update('name_ar', e.target.value)}
              className="w-full bg-dark-800 border border-dark-500 text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-brand-400" />
          </div>
          <div>
            <label className="block text-slate-400 text-sm mb-1">اسم إنجليزي</label>
            <input type="text" value={form.name ?? ''} onChange={(e) => update('name', e.target.value)}
              className="w-full bg-dark-800 border border-dark-500 text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-brand-400" />
          </div>
          <div>
            <label className="block text-slate-400 text-sm mb-1">السعر</label>
            <input type="number" step="0.01" value={form.price ?? ''} onChange={(e) => update('price', parseFloat(e.target.value))}
              className="w-full bg-dark-800 border border-dark-500 text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-brand-400" />
          </div>
          <div>
            <label className="block text-slate-400 text-sm mb-1">رابط المعاينة</label>
            <input type="url" value={form.preview_url ?? ''} onChange={(e) => update('preview_url', e.target.value)}
              className="w-full bg-dark-800 border border-dark-500 text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-brand-400" />
          </div>
          <div>
            <label className="block text-slate-400 text-sm mb-1">رابط ZIP</label>
            <input type="url" value={form.zip_file_url ?? ''} onChange={(e) => update('zip_file_url', e.target.value)}
              className="w-full bg-dark-800 border border-dark-500 text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-brand-400" />
          </div>
          <div>
            <label className="block text-slate-400 text-sm mb-1">رابط الغلاف</label>
            <input type="url" value={form.thumbnail_url ?? ''} onChange={(e) => update('thumbnail_url', e.target.value)}
              className="w-full bg-dark-800 border border-dark-500 text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-brand-400" />
          </div>
        </div>
        <div>
          <label className="block text-slate-400 text-sm mb-1">الوصف</label>
          <textarea rows={3} value={form.description_ar ?? ''} onChange={(e) => update('description_ar', e.target.value)}
            className="w-full bg-dark-800 border border-dark-500 text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-brand-400 resize-none" />
        </div>
        <div>
          <label className="block text-slate-400 text-sm mb-1">الميزات (سطر لكل ميزة)</label>
          <textarea rows={4} value={form.features_ar_text ?? ''} onChange={(e) => update('features_ar_text', e.target.value)}
            className="w-full bg-dark-800 border border-dark-500 text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-brand-400 resize-none" />
        </div>
        <div>
          <label className="block text-slate-400 text-sm mb-1">التقنيات</label>
          <input type="text" value={form.tech_stack_text ?? ''} onChange={(e) => update('tech_stack_text', e.target.value)}
            className="w-full bg-dark-800 border border-dark-500 text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-brand-400" />
        </div>
        <div className="flex items-center gap-2">
          <input type="checkbox" id="active" checked={form.is_active ?? true} onChange={(e) => update('is_active', e.target.checked)} className="w-4 h-4 accent-brand-400" />
          <label htmlFor="active" className="text-slate-400 text-sm">منتج نشط</label>
          <input type="checkbox" id="featured" checked={form.is_featured ?? false} onChange={(e) => update('is_featured', e.target.checked)} className="w-4 h-4 accent-brand-400 mr-4" />
          <label htmlFor="featured" className="text-slate-400 text-sm">منتج مميز</label>
        </div>
        <button type="submit" disabled={saving}
          className="w-full bg-gradient-to-r from-brand-500 to-brand-400 text-dark-900 font-bold py-3 rounded-xl hover:opacity-90 disabled:opacity-60">
          {saving ? 'جاري الحفظ...' : 'حفظ التعديلات'}
        </button>
      </form>
    </div>
  );
}
