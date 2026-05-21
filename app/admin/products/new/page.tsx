'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import toast from 'react-hot-toast';

export default function NewProduct() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({
    name: '', name_ar: '', description: '', description_ar: '',
    price: '', type: 'store', preview_url: '', zip_file_url: '',
    thumbnail_url: '', instructions_url: '',
    features_ar: '', tech_stack: '', is_featured: false,
  });

  function update(field: string, value: string | boolean) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    const adminKey = sessionStorage.getItem('admin_key') ?? '';

    const payload = {
      ...form,
      price: parseFloat(form.price),
      features_ar: form.features_ar.split('\n').filter(Boolean),
      features: form.features_ar.split('\n').filter(Boolean),
      tech_stack: form.tech_stack.split(',').map((s) => s.trim()).filter(Boolean),
    };

    try {
      const res = await fetch('/api/products', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'x-admin-key': adminKey },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error);
      toast.success('تم إضافة المنتج بنجاح!');
      router.push('/admin/products');
    } catch (err: unknown) {
      toast.error(err instanceof Error ? err.message : 'حدث خطأ');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-white mb-6">إضافة منتج جديد</h1>
      <form onSubmit={handleSubmit} className="bg-dark-700 border border-dark-500 rounded-2xl p-6 space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-slate-400 text-sm mb-1">اسم المنتج (عربي) *</label>
            <input required type="text" value={form.name_ar} onChange={(e) => update('name_ar', e.target.value)}
              className="w-full bg-dark-800 border border-dark-500 text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-brand-400" />
          </div>
          <div>
            <label className="block text-slate-400 text-sm mb-1">اسم المنتج (إنجليزي) *</label>
            <input required type="text" value={form.name} onChange={(e) => update('name', e.target.value)}
              className="w-full bg-dark-800 border border-dark-500 text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-brand-400" />
          </div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-slate-400 text-sm mb-1">السعر ($) *</label>
            <input required type="number" step="0.01" value={form.price} onChange={(e) => update('price', e.target.value)}
              className="w-full bg-dark-800 border border-dark-500 text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-brand-400" />
          </div>
          <div>
            <label className="block text-slate-400 text-sm mb-1">النوع</label>
            <select value={form.type} onChange={(e) => update('type', e.target.value)}
              className="w-full bg-dark-800 border border-dark-500 text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-brand-400">
              <option value="store">متجر</option>
              <option value="template">قالب</option>
              <option value="service">خدمة</option>
            </select>
          </div>
          <div className="flex items-center gap-2 mt-6">
            <input type="checkbox" id="featured" checked={form.is_featured} onChange={(e) => update('is_featured', e.target.checked)}
              className="w-4 h-4 accent-brand-400" />
            <label htmlFor="featured" className="text-slate-400 text-sm">منتج مميز</label>
          </div>
        </div>

        <div>
          <label className="block text-slate-400 text-sm mb-1">الوصف (عربي)</label>
          <textarea rows={3} value={form.description_ar} onChange={(e) => update('description_ar', e.target.value)}
            className="w-full bg-dark-800 border border-dark-500 text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-brand-400 resize-none" />
        </div>

        <div>
          <label className="block text-slate-400 text-sm mb-1">الميزات (سطر لكل ميزة)</label>
          <textarea rows={4} value={form.features_ar} onChange={(e) => update('features_ar', e.target.value)}
            placeholder="نظام إدارة متكامل&#10;دعم متعدد اللغات"
            className="w-full bg-dark-800 border border-dark-500 text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-brand-400 resize-none" />
        </div>

        <div>
          <label className="block text-slate-400 text-sm mb-1">التقنيات (مفصولة بفواصل)</label>
          <input type="text" value={form.tech_stack} onChange={(e) => update('tech_stack', e.target.value)}
            placeholder="Next.js, Supabase, Tailwind CSS"
            className="w-full bg-dark-800 border border-dark-500 text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-brand-400" />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-slate-400 text-sm mb-1">رابط المعاينة (Vercel)</label>
            <input type="url" value={form.preview_url} onChange={(e) => update('preview_url', e.target.value)}
              className="w-full bg-dark-800 border border-dark-500 text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-brand-400" />
          </div>
          <div>
            <label className="block text-slate-400 text-sm mb-1">رابط صورة الغلاف</label>
            <input type="url" value={form.thumbnail_url} onChange={(e) => update('thumbnail_url', e.target.value)}
              className="w-full bg-dark-800 border border-dark-500 text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-brand-400" />
          </div>
          <div>
            <label className="block text-slate-400 text-sm mb-1">رابط ملف ZIP (Supabase Storage)</label>
            <input type="url" value={form.zip_file_url} onChange={(e) => update('zip_file_url', e.target.value)}
              className="w-full bg-dark-800 border border-dark-500 text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-brand-400" />
          </div>
          <div>
            <label className="block text-slate-400 text-sm mb-1">رابط ملف التعليمات</label>
            <input type="url" value={form.instructions_url} onChange={(e) => update('instructions_url', e.target.value)}
              className="w-full bg-dark-800 border border-dark-500 text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-brand-400" />
          </div>
        </div>

        <button type="submit" disabled={loading}
          className="w-full bg-gradient-to-r from-brand-500 to-brand-400 text-dark-900 font-bold py-3 rounded-xl hover:opacity-90 disabled:opacity-60">
          {loading ? 'جاري الحفظ...' : 'إضافة المنتج'}
        </button>
      </form>
    </div>
  );
}
