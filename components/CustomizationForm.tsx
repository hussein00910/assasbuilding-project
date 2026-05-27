'use client';
import { useState } from 'react';
import { Send, CheckCircle } from 'lucide-react';
import toast from 'react-hot-toast';

export default function CustomizationForm({ purchaseId }: { purchaseId: string }) {
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({
    customer_name: '',
    customer_email: '',
    request_details: '',
    color_changes: '',
    new_sections: '',
    payment_gateway: '',
    domain_config: '',
    other_changes: '',
  });

  function update(field: string, value: string) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch('/api/customization-requests', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...form, purchase_id: purchaseId }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error);
      setSubmitted(true);
      toast.success('تم إرسال طلبك بنجاح!');
    } catch {
      toast.error('حدث خطأ، حاول مجدداً');
    } finally {
      setLoading(false);
    }
  }

  if (submitted) {
    return (
      <div className="mt-8 bg-green-500/10 border border-green-500/20 rounded-2xl p-8 text-center">
        <CheckCircle className="w-12 h-12 text-green-400 mx-auto mb-4" />
        <h3 className="text-xl font-bold text-white mb-2">تم استلام طلبك!</h3>
        <p className="text-slate-400">سنتواصل معك خلال 24 ساعة لبدء التنفيذ.</p>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="mt-8 bg-dark-700 border border-dark-500 rounded-2xl p-6 text-right space-y-4">
      <h3 className="text-xl font-bold text-white mb-2">نموذج طلب التعديل</h3>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-slate-400 text-sm mb-1">اسمك *</label>
          <input required type="text" value={form.customer_name} onChange={(e) => update('customer_name', e.target.value)}
            className="w-full bg-dark-800 border border-dark-500 text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-brand-400" />
        </div>
        <div>
          <label className="block text-slate-400 text-sm mb-1">بريدك *</label>
          <input required type="email" value={form.customer_email} onChange={(e) => update('customer_email', e.target.value)}
            className="w-full bg-dark-800 border border-dark-500 text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-brand-400" />
        </div>
      </div>

      <div>
        <label className="block text-slate-400 text-sm mb-1">وصف شامل للتعديلات المطلوبة *</label>
        <textarea required rows={3} value={form.request_details} onChange={(e) => update('request_details', e.target.value)}
          placeholder="اكتب هنا كل ما تريد تعديله بالتفصيل..."
          className="w-full bg-dark-800 border border-dark-500 text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-brand-400 resize-none" />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-slate-400 text-sm mb-1">تغيير الألوان</label>
          <input type="text" value={form.color_changes} onChange={(e) => update('color_changes', e.target.value)}
            placeholder="مثال: أزرق وأبيض"
            className="w-full bg-dark-800 border border-dark-500 text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-brand-400" />
        </div>
        <div>
          <label className="block text-slate-400 text-sm mb-1">بوابة الدفع المطلوبة</label>
          <input type="text" value={form.payment_gateway} onChange={(e) => update('payment_gateway', e.target.value)}
            placeholder="مثال: تبادل، Stripe"
            className="w-full bg-dark-800 border border-dark-500 text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-brand-400" />
        </div>
        <div>
          <label className="block text-slate-400 text-sm mb-1">أقسام جديدة مطلوبة</label>
          <input type="text" value={form.new_sections} onChange={(e) => update('new_sections', e.target.value)}
            placeholder="مثال: صفحة التواصل، مدونة"
            className="w-full bg-dark-800 border border-dark-500 text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-brand-400" />
        </div>
        <div>
          <label className="block text-slate-400 text-sm mb-1">الدومين المطلوب</label>
          <input type="text" value={form.domain_config} onChange={(e) => update('domain_config', e.target.value)}
            placeholder="مثال: mystore.com"
            className="w-full bg-dark-800 border border-dark-500 text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-brand-400" />
        </div>
      </div>

      <div>
        <label className="block text-slate-400 text-sm mb-1">تعديلات أخرى</label>
        <textarea rows={2} value={form.other_changes} onChange={(e) => update('other_changes', e.target.value)}
          className="w-full bg-dark-800 border border-dark-500 text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-brand-400 resize-none" />
      </div>

      <button type="submit" disabled={loading}
        className="w-full flex items-center justify-center gap-2 bg-gradient-to-r from-brand-500 to-brand-400 text-dark-900 font-bold py-3 rounded-xl hover:opacity-90 transition-opacity disabled:opacity-60">
        {loading ? <div className="w-5 h-5 border-2 border-dark-900 border-t-transparent rounded-full animate-spin" /> : <><Send className="w-4 h-4" /><span>إرسال الطلب</span></>}
      </button>
    </form>
  );
}
